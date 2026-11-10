"""Check, install, update and remove artefact plugins from a shell.

python -m app.domains.content.plugins validate <folder>
python -m app.domains.content.plugins install|update|sync <folder>

``sync`` installs the plugin when it is not installed and updates it otherwise.
python -m app.domains.content.plugins remove [--if-installed] <name>

``remove --if-installed`` does nothing for a name that was never installed or is already removed,
so a deploy can retire a plugin on every host.
python -m app.domains.content.plugins list
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from app.domains.content.plugins.plugin import Plugin
from app.domains.content.plugins.problems import errors_in
from app.domains.content.plugins.reader import folder_digest, read_plugins

_BY = "shell"


def _read(folder: Path) -> tuple[list[Plugin], str]:
    plugins, problems = read_plugins(folder)
    for problem in problems:
        print(problem)
    return ([] if errors_in(problems) else plugins), folder_digest(folder)


async def _run(command: str, target: str, *, if_installed: bool = False) -> int:
    """Install, update or remove against the database the app is set up for."""
    import app.db.metadata  # noqa: F401, PLC0415  (registers every ORM model; mappers need them all)
    from app.db.session import AsyncSessionLocal, engine  # noqa: PLC0415
    from app.domains.content.application.errors import ContentError  # noqa: PLC0415
    from app.domains.content.application.plugins import PluginInstaller  # noqa: PLC0415
    from app.domains.content.infrastructure.catalogue import (  # noqa: PLC0415
        build_content_catalogue,
    )
    from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins  # noqa: PLC0415

    installer = PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())
    try:
        async with AsyncSessionLocal() as db:
            if command == "list":
                for found in await installer.installed(db):
                    where = f"{found.type_slug} {found.status.value}"
                    print(f"{found.name} {found.version} r{found.revision} {where}")
                return 0
            if command == "remove":
                if if_installed and target not in {
                    found.name for found in await installer.installed(db) if found.installed
                }:
                    print(f"{target}: not installed")
                    return 0
                done = [await installer.remove(db, target, _BY)]
            else:
                plugins, digest = _read(Path(target))
                if not plugins:
                    return 1
                act = {"install": installer.install, "update": installer.update}.get(
                    command, installer.sync
                )
                done = [await act(db, plugin, digest, _BY) for plugin in plugins]
            await db.commit()
        for one in done:
            print(f"{one.name}: {one.status.value}, revision {one.revision}, type {one.type_slug}")
        return 0
    except ContentError as error:
        print(f"error: {error.detail}")
        return 1
    finally:
        await engine.dispose()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "install", "update", "sync", "remove"):
        command = commands.add_parser(name)
        command.add_argument("target", type=str)
        if name == "remove":
            command.add_argument("--if-installed", action="store_true")
    commands.add_parser("list")
    arguments = parser.parse_args(argv)
    if arguments.command == "validate":
        plugins, _ = _read(Path(arguments.target))
        for plugin in plugins:
            print(f"{plugin.name}: valid ({plugin.slug}, {len(plugin.skills)} skills)")
        return 0 if plugins else 1
    return asyncio.run(
        _run(
            arguments.command,
            getattr(arguments, "target", ""),
            if_installed=getattr(arguments, "if_installed", False),
        )
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
