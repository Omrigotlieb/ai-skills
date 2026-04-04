#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_FILES = sorted(ROOT.rglob("*.md"))

LINK_RE = re.compile(r"!?[^\S\r\n]*\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"""<(?:a|img)\b[^>]*\b(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}
PLACEHOLDER_HOSTS = {"example.com", "www.example.com", "example.org", "www.example.org"}
PLACEHOLDER_GITHUB_PREFIXES = {
    "/example/",
    "/username/",
    "/your-username/",
    "/your-org/",
}


def strip_fenced_blocks(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    fence = ""

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue

        if not in_fence:
            lines.append(line)

    return "\n".join(lines)


def normalize_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.find(">")]

    match = re.match(r"""(\S+?)(?:\s+["'][^"']*["'])?$""", value)
    return match.group(1) if match else value


def slugify_heading(heading: str) -> str:
    text = heading.strip().rstrip("#").strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text)
    text = text.replace(" ", "-")
    return text.strip("-")


def collect_heading_slugs(path: Path) -> set[str]:
    text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
    counts: defaultdict[str, int] = defaultdict(int)
    slugs: set[str] = set()

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue

        base = slugify_heading(match.group(2))
        if not base:
            continue

        index = counts[base]
        counts[base] += 1
        slug = base if index == 0 else f"{base}-{index}"
        slugs.add(slug)

    return slugs


def extract_links(path: Path) -> list[str]:
    text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
    links = [normalize_destination(match.group(1)) for match in LINK_RE.finditer(text)]
    links.extend(match.group(1).strip() for match in HTML_LINK_RE.finditer(text))
    return links


def is_placeholder_external(link: str) -> bool:
    parsed = urlparse(link)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if host in PLACEHOLDER_HOSTS:
        return True

    if host == "github.com" and any(path.startswith(prefix) for prefix in PLACEHOLDER_GITHUB_PREFIXES):
        return True

    return False


def validate_markdown() -> list[str]:
    errors: list[str] = []
    heading_cache: dict[Path, set[str]] = {}

    for md_file in MARKDOWN_FILES:
        for link in extract_links(md_file):
            parsed = urlparse(link)

            if parsed.scheme in EXTERNAL_SCHEMES:
                if is_placeholder_external(link):
                    errors.append(f"{md_file.relative_to(ROOT)}: placeholder URL -> {link}")
                continue

            if parsed.scheme or parsed.netloc:
                continue

            target_path = parsed.path
            fragment = parsed.fragment

            if not target_path:
                resolved = md_file
            else:
                resolved = (md_file.parent / unquote(target_path)).resolve()

            if not resolved.exists():
                errors.append(
                    f"{md_file.relative_to(ROOT)}: missing local target '{target_path}' in link '{link}'"
                )
                continue

            if fragment and resolved.suffix.lower() == ".md":
                if resolved not in heading_cache:
                    heading_cache[resolved] = collect_heading_slugs(resolved)

                if fragment not in heading_cache[resolved]:
                    errors.append(
                        f"{md_file.relative_to(ROOT)}: missing anchor '#{fragment}' in '{resolved.relative_to(ROOT)}'"
                    )

    return errors


def main() -> int:
    errors = validate_markdown()
    if errors:
        print("Docs validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Docs validation passed for {len(MARKDOWN_FILES)} Markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
