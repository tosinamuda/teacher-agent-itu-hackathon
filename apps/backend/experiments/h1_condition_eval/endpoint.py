"""What an LLM endpoint actually offers.

A Bedrock model id is not guessable — ``openai.gpt-oss-120b-1:0``,
``us.anthropic.claude-sonnet-5-...`` — and naming one wrong fails a whole run at the
first call. This asks the endpoint, which costs nothing: it is a metadata request and
consumes no tokens.

**Bedrock core and mantle do not serve the same catalogue.** A model on one need not be
on the other, so the judge and the generator may have to sit on different endpoints —
which is what ``JUDGE_API_BASE`` is for. Point ``--base`` at each in turn to see what
each has before choosing.

    uv run python -m experiments.h1_condition_eval.endpoint --like claude
    uv run python -m experiments.h1_condition_eval.endpoint \
        --base https://bedrock-core... --like claude
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv

from app.infra.dspy_lm import custom_endpoint
from app.infra.llm_models import HOSTS, hosted_at

HERE = Path(__file__).parent


def _key_for(base: str) -> str:
    """The credential the declared host at ``base`` uses, or "" if none is declared.

    ``--base`` used to swap the URL and keep the configured key, which sends the
    generator's credential to somebody else's endpoint. The reply is a 401 naming a key
    that is valid — for the host it was issued by — and reads exactly like an expired
    key for the host being asked. That cost a wrong conclusion once.
    """
    root = base.removesuffix("/chat/completions").rstrip("/").removesuffix("/v1")
    for host in HOSTS.values():
        if host.base and root.startswith(host.base.rstrip("/")):
            for name in host.key_env:
                if value := os.environ.get(name):
                    return value
    return ""


def offered(base: str = "") -> list[str]:
    """Every model id an endpoint serves. Defaults to the configured one."""
    endpoint = custom_endpoint()
    if base:
        endpoint = {
            **endpoint,
            "api_base": base.removesuffix("/chat/completions").rstrip("/"),
            "api_key": _key_for(base) or endpoint.get("api_key", ""),
        }
    if not endpoint.get("api_base") or not endpoint.get("api_key"):
        raise SystemExit(
            "No endpoint configured. Set LLM_API_BASE and LLM_API_KEY — see "
            "src/app/infra/dspy_lm.custom_endpoint."
        )
    url = endpoint["api_base"].rstrip("/") + "/models"
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {endpoint['api_key']}"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"HTTP {error.code} from {url}: {error.read()[:300]!r}") from error
    return sorted(str(model.get("id", "?")) for model in payload.get("data", []))


#: The two wire formats mantle routes, and the path each lives at. Discovered by probing:
#: a routed path rejects a bad body with 400, an unrouted one 404s with an empty body.
#: ``/v1/messages`` — the obvious guess, and what litellm builds from a ``/v1`` base — is
#: NOT routed here. Anthropic sits under ``/anthropic``, exactly as it does on DeepSeek.
API_PATH = {"openai": "/v1/chat/completions", "anthropic": "/anthropic/v1/messages"}


def _wire(model_id: str) -> str:
    """Which format serves *model_id* — its vendor prefix decides."""
    return "anthropic" if model_id.startswith("anthropic.") else "openai"


def _probe(root: str, key: str, model_id: str) -> tuple[str, str]:
    """One minimal call. Returns (verdict, detail); costs a handful of tokens."""
    wire = _wire(model_id)
    body: dict[str, object] = {
        "model": model_id,
        "max_tokens": 200,
        "messages": [{"role": "user", "content": "say OK"}],
    }
    request = urllib.request.Request(
        root + API_PATH[wire],
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = json.loads(error.read() or b"{}").get("error", {})
        return detail.get("type") or detail.get("code") or f"http_{error.code}", detail.get(
            "message", ""
        )[:90]
    except Exception as error:  # noqa: BLE001 — a probe reports, it does not raise
        return "unreachable", str(error)[:90]
    if wire == "anthropic":
        return "callable", "".join(b.get("text", "") for b in payload.get("content", []))[:40]
    choice = (payload.get("choices") or [{}])[0].get("message") or {}
    return "callable", (choice.get("content") or choice.get("reasoning") or "")[:40]


def entitlements(base: str = "") -> list[tuple[str, str, str]]:
    """(model, verdict, detail) for every catalogue id, probed with a real call.

    ``/v1/models`` lists what mantle KNOWS, not what this account may CALL — the two
    differ sharply, and nothing in the listing says so. Every Anthropic id is listed and
    every one returns ``permission_error``. Discovering that from a judged run means
    discovering it 72 calls in.
    """
    endpoint = custom_endpoint()
    root = (base or endpoint["api_base"]).rstrip("/").removesuffix("/v1").removesuffix("/anthropic")
    ids = offered(base)
    with ThreadPoolExecutor(max_workers=8) as pool:
        verdicts = list(pool.map(lambda m: _probe(root, endpoint["api_key"], m), ids))
    return [(model, *verdict) for model, verdict in zip(ids, verdicts, strict=True)]


def unserved(base: str = "") -> list[tuple[str, str, str]]:
    """Every ``MODELS`` entry whose ``call_as`` this endpoint does not serve.

    A declared id is a guess until something checks it. Two of the first five were the
    AWS console's spelling rather than mantle's — ``us.anthropic.claude-sonnet-5`` and
    ``openai.gpt-oss-120b-1:0`` — and each would have failed a whole run at its first
    call, as a 404 that reads like a broken endpoint rather than a typo. This costs no
    tokens, so it can run before anything expensive does.

    Only the models declared to live on this host are checked — see ``Model.host``.
    DeepSeek's v4-flash is absent from mantle by design, and a check that fails in the
    normal case is a check nobody reads.

    Returns (family, declared id, nearest served id) for each miss.
    """
    where = base or custom_endpoint().get("api_base", "")
    mine = hosted_at(where)
    served = set(offered(base))
    misses = []
    for family, model in mine.items():
        ident = model.call_as.partition("/")[2]
        stem = ident.split(".", 1)[-1].replace("-", "").replace(".", "").lower()
        if ident in served:
            continue
        near = [s for s in served if stem[:12] in s.replace("-", "").replace(".", "").lower()]
        misses.append((family, ident, ", ".join(sorted(near)) or "nothing similar"))
    return misses


def price(model: str) -> tuple[float, float] | None:
    """(input, output) dollars per million tokens, from litellm's own table.

    litellm ships pricing for ~3000 ids and keeps it current, so this is read rather
    than typed. A hand-kept table is a second thing to get wrong, and the cost is what
    a spending decision turns on.
    """
    import litellm

    for candidate in (model, model.rsplit("/", 1)[-1]):
        info = litellm.model_cost.get(candidate)
        if info and info.get("input_cost_per_token"):
            return (
                float(info["input_cost_per_token"]) * 1e6,
                float(info.get("output_cost_per_token") or 0) * 1e6,
            )
    return None


def judging_cost(run_label: str, model: str) -> str:
    """What one blinded pass over a run's packets would cost, before running it."""
    packets = HERE / "runs" / run_label / "rating" / "packets"
    if not packets.is_dir():
        return f"no packets for {run_label!r} — build them with rater_packets first"
    sizes = [len(path.read_text(encoding="utf-8")) for path in packets.glob("*.md")]
    if not sizes:
        return f"no packets for {run_label!r}"
    # ~4 characters to a token, and a judgment is four dimensions of score, evidence
    # and rationale — about 900 output tokens, measured on the passes already run.
    tokens_in = sum(sizes) / 4 / 1e6
    tokens_out = len(sizes) * 900 / 1e6
    rate = price(model)
    if rate is None:
        return (
            f"{len(sizes)} packets, ~{tokens_in:.3f}M in / {tokens_out:.3f}M out — "
            f"litellm has no price for {model!r}, so this cannot be costed"
        )
    return (
        f"{len(sizes)} packets, ~{tokens_in:.3f}M in / {tokens_out:.3f}M out\n"
        f"  {model} at ${rate[0]:.2f}/${rate[1]:.2f} per M "
        f"-> ${tokens_in * rate[0] + tokens_out * rate[1]:.2f} for one pass"
    )


def main() -> int:
    # Every entry point loads it for itself. litellm happens to load .env when IT is
    # imported, which made this work by luck of import order — and stopped working the
    # moment a caller reached the config without touching litellm first.
    load_dotenv(override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--like", default="", help="only ids containing this")
    parser.add_argument(
        "--base", default="", help="ask this endpoint instead of the configured one"
    )
    parser.add_argument("--cost", default="", metavar="RUN", help="cost a judge pass over RUN")
    parser.add_argument(
        "--check", action="store_true", help="verify every llm_models id is served here"
    )
    parser.add_argument(
        "--callable",
        action="store_true",
        help="probe every catalogue id with a real minimal call (a few tokens each)",
    )
    parser.add_argument("--model", default="", help="which model to cost")
    args = parser.parse_args()
    if args.callable:
        rows = entitlements(args.base)
        for model, verdict, detail in rows:
            mark = "CALLABLE" if verdict == "callable" else verdict
            print(f"  {mark:<23} {model:<38} {detail.strip()[:34]!r}")
        yes = [m for m, v, _ in rows if v == "callable"]
        print(f"\n{len(yes)}/{len(rows)} of the catalogue is callable on this account")
        return 0
    if args.check:
        where = args.base or custom_endpoint().get("api_base", "")
        mine = hosted_at(where)
        misses = unserved(args.base)
        for family, ident, near in misses:
            print(f"  MISSING  {family}: {ident!r} is not served. Nearest: {near}")
        for family, declared in sorted(mine.items()):
            if family not in {m[0] for m in misses}:
                print(f"  ok       {family}: {declared.call_as}")
        print(f"{len(mine) - len(misses)}/{len(mine)} models declared for {where} are served")
        return 1 if misses else 0
    if args.cost:
        if not args.model:
            raise SystemExit("--cost needs --model")
        print(judging_cost(args.cost, args.model))
        return 0
    ids = [model for model in offered(args.base) if args.like.lower() in model.lower()]
    print(f"{len(ids)} model(s) on {args.base or 'the configured endpoint'}:")
    for model in ids:
        print(f"  {model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
