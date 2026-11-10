"""The skills a writer reads: every skill, one skill, and the files of the plugin behind a type."""

from __future__ import annotations

from collections.abc import Callable

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceError

from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content_engine.mcp.caller import caller, permit
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload, as_payload
from app.shared.json_types import JsonObject


def add_skill_resources(
    server: MCPServer, catalogue: Callable[[], ContentCatalogue], sessions: Sessions
) -> None:
    @server.resource("skills://{?search}", mime_type="application/json")
    async def skills(ctx: Context, search: str | None = None) -> list[Payload]:
        """Every skill at its latest revision, with its name and when to use it.

        ``?search=`` keeps the skills whose name or description holds the words.
        """
        async with sessions() as db:
            await refusing(permit(db, await caller(db, ctx.headers), "read"), ResourceError)
            words = (search or "").lower()
            return [
                as_payload(s.summary())
                for s in await catalogue().skills.skills(db)
                if words in f"{s.name} {s.description}".lower()
            ]

    @server.resource("skill://{slug}{?revision}", mime_type="application/json")
    async def skill(slug: str, ctx: Context, revision: int | None = None) -> Payload:
        """One skill with its instructions and reference files, at ``?revision=`` or its latest."""
        async with sessions() as db:
            await refusing(permit(db, await caller(db, ctx.headers), "read"), ResourceError)
            found = await refusing(catalogue().skills.at(db, slug, revision), ResourceError)
            return as_payload(found.document())

    @server.resource("plugin-skills://{type}{?spec_revision}", mime_type="application/json")
    async def plugin_skills(type: str, ctx: Context, spec_revision: int | None = None) -> Payload:
        """The skill files of the plugin that made a type, as installed, to copy as they are.

        ``?spec_revision=`` names the spec revision the plugin made; the current one otherwise.
        """
        async with sessions() as db:
            await refusing(permit(db, await caller(db, ctx.headers), "read"), ResourceError)
            types = catalogue()
            if spec_revision is None:
                spec_revision = (await refusing(types.current(db, type), ResourceError)).revision
            found = await types.plugin_files(db, type, spec_revision)
            if found is None:
                raise ResourceError(f"no plugin made {type} at spec revision {spec_revision}")
            files: JsonObject = {
                path: text for path, text in found.files.items() if path.startswith("skills/")
            }
            return as_payload({"plugin": found.name, "revision": found.revision, "files": files})
