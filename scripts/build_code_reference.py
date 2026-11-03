"""Generate a scope-based source reference without reading secrets or runtime media."""

import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "job": "Temporary episode with metadata, files, approvals and cancellation resources.",
    "jobs": "In-memory registry indexed by random job ID; lost on restart.",
    "jid": "Random public job ID; a separate secret token is required.",
    "token": "Secret authentication value held in memory and sent in X-Job-Token.",
    "path": "Controlled filesystem location, never an uploaded filename.",
    "design": "Validated episode appearance/encoding settings or unsaved browser draft.",
    "settings": "Backend environment configuration; see CONFIGURATION.md.",
    "meta": "Inspected audio metadata including duration and selected stream.",
    "cues": "Ordered subtitle intervals with optional estimated word timing.",
    "words": "Validated recognized word intervals used for grouping/highlighting.",
    "warnings": "Nonfatal review messages such as overlap or estimated timing.",
    "state": "Lifecycle enum, independent of interface language.",
    "phase": "Human-readable description of the current operation.",
    "progress": "Processed fraction from 0 to 1, or None/null for indeterminate work.",
    "error": "Safe explanatory failure text; must not expose secrets or raw stderr.",
    "expires": "Idle expiry in Unix seconds; polling must not extend it.",
    "active_deadline": "Absolute Unix deadline for an active operation.",
    "approved": "Whether the current background was explicitly reviewed.",
    "preview_approved": "Whether the current preview was explicitly reviewed.",
    "artifacts": "Available output kinds; stale renders are discarded after edits.",
    "cancel": "Backend cancellation event or frontend operation name, according to scope.",
    "process": "Supervised child process; stop it before releasing the worker.",
    "readers": "Active download leases that prevent premature cleanup.",
    "deleting": "Deferred deletion flag; cleanup waits for readers/workers.",
    "root": "Exclusive temporary root or repository root; inspect the initializer.",
    "lock": "Reentrant lock protecting shared registry changes.",
    "queue": "Bounded FIFO of pending operations consumed by one worker.",
    "stop": "Shutdown event checked by worker and cleanup loops.",
    "provider": "Image provider; tests replace it with a fake to avoid charges.",
    "request": "HTTP request containing headers and a streamed body.",
    "response": "Outgoing HTTP response or inspected fetch result.",
    "scope": "ASGI context with path, headers and protocol metadata.",
    "receive": "ASGI callable reading incoming body events.",
    "send": "ASGI callable sending outgoing response events.",
    "headers": "HTTP headers, including origin or authentication as needed.",
    "origin": "Browser origin checked against the local allowlist.",
    "total": "Accumulated incoming body bytes.",
    "kind": "Allowlisted operation/artifact key, not an arbitrary filename.",
    "start": "Start time in seconds; in multipart callbacks, byte-slice start index.",
    "end": "Interval end in seconds; in multipart callbacks, byte-slice end index.",
    "duration": "Audio or clip length in seconds.",
    "args": "Checked subprocess arguments or parsed CLI options, according to scope.",
    "update": "Callback reporting real render progress.",
    "text": "Subtitle/title text; escape before ASS insertion and never translate user content.",
    "srt": "SRT under review; editing intentionally discards word alignment.",
    "original": "Last saved SRT text for dirty-state comparison.",
    "font_key": "Allowlisted font ID used for real font measurement.",
    "width": "Available width in video pixels for text wrapping.",
    "bold": "Whether to select the actual Bold font/style.",
    "x": "Horizontal title coordinate in video pixels, when used in make_ass.",
    "y": "Vertical title coordinate in video pixels, when used in make_ass.",
    "margin": "Canvas inset measured in video pixels.",
    "pcm": "Temporary mono 16 kHz float32 audio for local inference.",
    "result": "Result of the operation/parser/API named by its assignment.",
    "data": "Payload being parsed/transferred; validate before trusting fields.",
    "busy": "Browser request-in-flight flag preventing duplicate actions.",
    "active": "Whether the job is queued/running/cancelling.",
    "disabled": "Combined gate for busy, active or unavailable episodes.",
    "dirty": "Whether draft settings/text differ from the saved version.",
    "step": "Zero-based Files/Design/Preview/Export workflow index.",
    "revision": "Cache-busting counter incremented when artifacts/settings change.",
    "unavailable": "Whether polling/action detected a missing/expired/invalid job.",
    "subtitleMode": "Initial subtitle source: upload or generate.",
    "language": "Spoken audio language sent to Whisper, not interface locale.",
    "transcriptionModel": "Local Whisper Tiny/Base selection.",
    "designMethod": "Manual setup or JSON-import choice.",
    "importedDesign": "Whether JSON settings were successfully imported.",
    "savedDesign": "Whether the current design has a successful save confirmation.",
    "caps": "Backend dependency/limit snapshot used to enable features.",
    "heading": "React ref used to focus the newly selected workflow heading.",
    "locale": "Interface language en/es; does not translate episode content.",
    "theme": "Interface-only Classic/Studio preference.",
    "catalog": "Spanish UI keys mapped to English display strings.",
    "reverse": "English-to-Spanish lookup for stored translated UI errors.",
    "listeners": "Subscribers notified when the locale store changes.",
    "storageKey": "Preference storage key; never contains episode tokens/media.",
    "reload": "Counter triggering an explicit subtitle refetch.",
    "current": "Async cleanup guard against stale/unmounted SRT updates.",
    "timer": "Polling interval handle cleared when the effect is disposed.",
    "stopped": "Effect cleanup guard preventing stale polling state updates.",
    "i": "Zero-based iteration index local to the current loop.",
    "self": "The current Python class instance.",
}


def meaning(name):
    """Explain a domain variable or a React setter; use source expressions for other locals."""
    if name.startswith("set") and len(name) > 3:
        return (
            "React state setter for "
            + name[3:4].lower()
            + name[4:]
            + ". Schedules a rerender, not a server mutation."
        )
    return ROLES.get(
        name.removeprefix("self."),
        "Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.",
    )


def cell(value):
    """Escape source excerpts for a Markdown table."""
    return str(value).replace("|", r"\|").replace("\n", " ")[:200]


def python_module(path):
    """Inventory Python declarations, parameters and assignments by their lexical scope."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    relative = path.relative_to(ROOT).as_posix()
    lines = [f"## {relative}", "", ast.get_docstring(tree) or "Repository utility module.", ""]

    def walk(node, scope="module"):
        """Render one lexical scope and recursively document nested declarations."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            scope = node.name if scope == "module" else scope + "." + node.name
            signature = (
                ast.unparse(node.args)
                if hasattr(node, "args")
                else ", ".join(ast.unparse(b) for b in node.bases)
            )
            lines.extend(
                [
                    f"### `{scope}({signature})`",
                    "",
                    ast.get_docstring(node) or "See the scoped implementation and assignments below.",
                    "",
                    f"Source: [{relative}:{node.lineno}](../{relative}).",
                    "",
                ]
            )
            if hasattr(node, "args"):
                for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                    lines.append(f"- `{arg.arg}`: {meaning(arg.arg)}")
                lines.append("")
        variables = []
        definitions = []

        def visit(item):
            """Collect assignments while keeping nested function/class scopes separate."""
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definitions.append(item)
                return
            if isinstance(
                item, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.For, ast.AsyncFor, ast.comprehension)
            ):
                targets = item.targets if isinstance(item, ast.Assign) else [item.target]
                value = getattr(item, "value", None) or getattr(item, "iter", None)
                for target in targets:
                    for sub in ast.walk(target):
                        if isinstance(sub, (ast.Name, ast.Attribute)) and isinstance(sub.ctx, ast.Store):
                            variables.append(
                                (
                                    ast.unparse(sub),
                                    getattr(item, "lineno", 0),
                                    ast.unparse(value) if value else "annotation / loop binding",
                                )
                            )
            if isinstance(item, ast.ExceptHandler) and item.name:
                variables.append((item.name, item.lineno, "caught exception"))
            for child in ast.iter_child_nodes(item):
                visit(child)

        for child in ast.iter_child_nodes(node):
            visit(child)
        if variables:
            lines.extend(
                [
                    "| Variable / attribute | Explanation | Initializer / assignment excerpt |",
                    "| --- | --- | --- |",
                ]
            )
            seen = set()
            for name, line, value in sorted(variables, key=lambda x: x[1]):
                if name not in seen:
                    seen.add(name)
                    lines.append(f"| `{cell(name)}` | {meaning(name)} | `{cell(value)}` |")
            lines.append("")
        for definition in definitions:
            walk(definition, scope)

    walk(tree)
    return lines


def main():
    """Generate docs/CODE_REFERENCE.md from application and utility source, not runtime files."""
    lines = [
        "# Source code reference",
        "",
        "Generated inventory of application/utility classes, named functions, parameters and assigned variables by lexical scope. Read JUNIOR_GUIDE.md first for a guided walkthrough. Test fixture internals, imported dependencies and third-party code are outside this inventory. Tiny loop locals are described by their source assignment rather than fictional domain meanings. Source excerpts remain exact code, so legacy Spanish message keys are code, not English documentation prose.",
        "",
        "Regenerate with `python scripts/build_code_reference.py` after installing frontend dependencies. Source line numbers are navigation hints. See CONFIGURATION.md for environment variables and DESIGN_CONTROLS.md for Design field units/bounds.",
        "",
    ]
    paths = sorted((ROOT / "backend/app").glob("*.py")) + sorted((ROOT / "scripts").glob("*.py"))
    for path in paths:
        if path.name != "__init__.py":
            lines.extend(python_module(path))
    result = subprocess.run(
        ["node", str(ROOT / "scripts/source_symbols.cjs")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    for module in json.loads(result.stdout):
        lines.extend(
            [
                "## " + module["file"],
                "",
                "| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |",
                "| --- | --- | --- | --- |",
            ]
        )
        for symbol in module["symbols"]:
            explanation = symbol["purpose"] or meaning(symbol["name"])
            lines.append(
                f"| `{cell(symbol['scope'] + '.' + symbol['name'])}` | {symbol['kind']} | {explanation} | `{cell(symbol['signature'])}` |"
            )
        lines.append("")
    (ROOT / "docs/CODE_REFERENCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Generated docs/CODE_REFERENCE.md")


if __name__ == "__main__":
    main()
