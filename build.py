#!/usr/bin/env python3
"""
Free Resume Pack build script.

One script, all local, no accounts:

  1. Fill in your details:  data/my-details.json   (ships with sample text)
  2. Build:                 python3 build.py
  3. Look in:               Printables/            (nine polished PDFs)

Optional flags:

  --variants classic,modern,pivot-story   build only some styles
  --docs resume,cover-letter,references   build only some documents
  --data PATH                             use a different details file
  --out PATH                              write PDFs somewhere else
  --keep-html                             also save the filled-in HTML files
                                          (open one in a browser and use
                                          "Print to PDF" if you prefer that)

Tests use the same functions this script calls: see tests/test_build.py.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html as html_module
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
DEFAULT_DATA = ROOT / "data" / "my-details.json"
DEFAULT_OUT = ROOT / "Printables"

VARIANTS = ["classic", "modern", "pivot-story"]
DOCS = ["resume", "cover-letter", "references"]

LIST_KEY_SUFFIX = "_bullets"
TODAY_KEY = "today"
TOKEN_RE = re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")
KEY_NAME_RE = re.compile(r"[a-z][a-z0-9_]*")

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


class BuildError(Exception):
    """A plain-English message shown to the user, instead of a stack trace."""


def today_text() -> str:
    now = dt.date.today()
    return f"{MONTHS[now.month - 1]} {now.day}, {now.year}"


def load_values(data_path: Path) -> dict:
    """
    Read the details file. Keys are the {{tokens}} used in the templates.
    Values are strings, or lists of strings (lists feed the *_bullets keys).
    """
    if not data_path.exists():
        raise BuildError(f"Couldn't find the details file: {data_path}")

    try:
        raw = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise BuildError(
            f"{data_path.name} isn't valid JSON yet: {err.msg} "
            f"(line {err.lineno}, column {err.colno}). "
            "That's usually a quote or comma that got left off. Compare what you "
            "changed against the sample text further up in the file."
        )

    if not isinstance(raw, dict):
        raise BuildError(
            f"{data_path.name} should hold one big block of settings, "
            "starting with { and ending with }."
        )

    values: dict = {}
    for key, value in raw.items():
        if str(key).startswith("_"):
            continue  # keys starting with _ are comments the templates ignore
        if not KEY_NAME_RE.fullmatch(str(key)):
            raise BuildError(
                f"Key names must be lowercase letters, numbers and underscores. "
                f"Fix the key '{key}' in {data_path.name}."
            )
        if isinstance(value, str):
            values[key] = value
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            values[key] = value
        else:
            raise BuildError(
                f"'{key}' should be a string or a list of strings. "
                "A list looks like: [\"first line\", \"second line\"]"
            )
    return values


def escaped_mapping(values: dict) -> dict:
    """
    Escape every value so symbols like < and & can't break the page, and turn
    list values into HTML list items for the *_bullets keys.
    """
    mapping: dict = {}
    for key, value in values.items():
        if isinstance(value, list):
            if key.endswith(LIST_KEY_SUFFIX):
                mapping[key] = "\n".join(
                    f"<li>{html_module.escape(item)}</li>" for item in value
                )
            else:
                mapping[key] = "<br>".join(html_module.escape(item) for item in value)
        else:
            mapping[key] = html_module.escape(value)
    mapping.setdefault(TODAY_KEY, today_text())
    return mapping


def substitute(template_text: str, mapping: dict, label: str) -> tuple[str, set]:
    """Replace every {{token}} in a template; raise if a token has no value."""
    missing: list = []
    used: set = set()

    def _replace(match):
        key = match.group(1)
        if key in mapping:
            used.add(key)
            return mapping[key]
        missing.append(key)
        return match.group(0)

    result = TOKEN_RE.sub(_replace, template_text)

    if missing:
        raise BuildError(
            f"{label} asks for details your file doesn't have yet:\n"
            + "\n".join(f"  - {key}" for key in sorted(missing))
            + "\nAdd them to your details file (match the spelling exactly) and build again."
        )
    if "{{" in result:
        raise BuildError(
            f"{label} still holds a double-brace {{token}} after filling in. "
            "Check the template's braces are written exactly like {{like_this}}."
        )
    return result, used


def read_template(template_path: Path) -> str:
    if not template_path.exists():
        available = "\n".join(
            f"  - {variant}/{doc}.html" for variant in VARIANTS for doc in DOCS
        )
        raise BuildError(
            f"Couldn't find the template: {template_path}\n"
            f"Available templates:\n{available}"
        )
    return template_path.read_text(encoding="utf-8")


def import_weasyprint():
    try:
        from weasyprint import HTML
        return HTML
    except ModuleNotFoundError:
        python_name = Path(sys.executable).name
        raise BuildError(
            "WeasyPrint isn't installed yet. It's the tool that turns the HTML "
            "templates into PDFs.\n"
            f"Install it with:  {python_name} -m pip install -r requirements.txt\n"
            "(run that from this folder; the README walks through it in plain English)"
        )


def page_count(pdf_path: Path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except ModuleNotFoundError:
        return None


def render_pdf(html_text: str, template_dir: Path, out_path: Path) -> None:
    HTML = import_weasyprint()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_text, base_url=str(template_dir)).write_pdf(target=str(out_path))


def build_document(
    variant: str,
    doc: str,
    values: dict,
    out_dir: Path,
    keep_html: bool = False,
) -> tuple[Path, set]:
    """Build one template; return (pdf path, set of tokens it used)."""
    template_path = TEMPLATES_DIR / variant / f"{doc}.html"
    label = f"{doc} - {variant} style"

    html_text, used = substitute(read_template(template_path), escaped_mapping(values), label)

    out_path = out_dir / f"{doc}-{variant}.pdf"
    render_pdf(html_text, template_path.parent, out_path)

    if keep_html:
        browser_css = f"../../templates/{variant}/{variant}.css"
        browser_html = html_text.replace(
            f'href="{variant}.css"', f'href="{browser_css}"', 1
        )
        html_out_path = out_dir / "html" / f"{doc}-{variant}.html"
        html_out_path.parent.mkdir(parents=True, exist_ok=True)
        html_out_path.write_text(browser_html, encoding="utf-8")

    return out_path, used


def combos(variants: list, docs: list):
    for variant in variants:
        for doc in docs:
            yield variant, doc


def build_all(
    variants: list,
    docs: list,
    data_path: Path = DEFAULT_DATA,
    out_dir: Path = DEFAULT_OUT,
    keep_html: bool = False,
) -> list:
    """Build every requested template; print friendly progress; return PDF paths."""
    values = load_values(data_path)
    pdf_paths: list = []
    tokens_used: set = set()

    total = len(variants) * len(docs)
    print(f"Building {total} PDF{'s' if total != 1 else ''} "
          f"into {out_dir} using {data_path}")

    for variant, doc in combos(variants, docs):
        out_path, used = build_document(variant, doc, values, out_dir, keep_html)
        tokens_used |= used
        pdf_paths.append(out_path)
        pages = page_count(out_path)
        size_kb = out_path.stat().st_size // 1024
        pages_text = f"{pages} page{'s' if pages != 1 else ''}, " if pages is not None else ""
        print(f"  [ok] {out_path.name}  ({pages_text}{size_kb} KB)")

    unused = [key for key in values if key not in tokens_used and key != TODAY_KEY]
    if unused:
        print(
            "Note: details your built styles didn't use (normal if you only built "
            "some styles; check spelling if this surprises you): "
            + ", ".join(sorted(unused))
        )
    return pdf_paths


def show_list() -> None:
    print("Styles and documents (each style has all three documents):")
    for variant in VARIANTS:
        print(f"  {variant}/")
        for doc in DOCS:
            print(f"    {doc}.html")
    print(f"\nDetails file: {DEFAULT_DATA}")
    print(f"Output folder: {DEFAULT_OUT}")


def parse_list_arg(text: str, choices: list, flag: str) -> list:
    items = [item.strip() for item in text.split(",") if item.strip()]
    if not items:
        raise argparse.ArgumentTypeError(
            f"{flag} needs names like: {','.join(choices)}"
        )
    for item in items:
        if item not in choices:
            raise argparse.ArgumentTypeError(
                f"unknown {flag} name '{item}'. Choices: {', '.join(choices)}"
            )
    return items


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the resume pack PDFs (local, no accounts).",
        epilog="Examples:  python3 build.py\n           python3 build.py --variants classic --docs resume",
    )
    parser.add_argument(
        "--variants", default=",".join(VARIANTS),
        help="comma-separated styles (default: all three)",
    )
    parser.add_argument(
        "--docs", default=",".join(DOCS),
        help="comma-separated documents (default: all three)",
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="details file (JSON)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output folder")
    parser.add_argument(
        "--keep-html", action="store_true",
        help="also save filled-in HTML files (for browser 'Print to PDF')",
    )
    parser.add_argument("--list", action="store_true", help="show the templates and stop")
    args = parser.parse_args(argv)

    if args.list:
        show_list()
        return 0

    try:
        variants = parse_list_arg(args.variants, VARIANTS, "--variants")
        docs = parse_list_arg(args.docs, DOCS, "--docs")
        build_all(variants, docs, data_path=args.data, out_dir=args.out, keep_html=args.keep_html)
    except argparse.ArgumentTypeError as err:
        print(f"Build didn't start: {err}", file=sys.stderr)
        return 2
    except BuildError as err:
        print(f"Build stopped: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
