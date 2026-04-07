#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "RECIPE_INDEX.md"
BOOK = ROOT / "RECIPE_BOOK.md"

BOOK_TITLE = "Recipe Test Kitchen Book"
BOOK_DESCRIPTION = "A working collection of recipes to try, recipes you've tested, and proven keepers."


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace("'", "").replace("’", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_index_sections(index_text: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in index_text.splitlines():
        if line.startswith("## "):
            current = {"title": line[3:].strip(), "paths": []}
            sections.append(current)
            continue

        if current is None:
            continue

        match = re.search(r"\((recipes/[^)]+\.md)\)", line)
        if match:
            paths = current["paths"]
            assert isinstance(paths, list)
            paths.append(ROOT / match.group(1))

    return sections


def fix_links(body: str, recipe_path: Path) -> str:
    link_re = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")

    def repl(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        target = target.strip()
        if target.startswith(("http://", "https://", "#", "/")):
            return match.group(0)

        rel = target.split(maxsplit=1)[0].strip("<>")
        resolved = (recipe_path.parent / rel).resolve()
        try:
            fixed = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return match.group(0)
        return f"{prefix}{fixed}{suffix}"

    return link_re.sub(repl, body)


def read_recipe(path: Path) -> tuple[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Recipe file not found: {path.relative_to(ROOT)}")

    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"Missing title heading in {path.relative_to(ROOT)}")

    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]).strip()
    return title, fix_links(body, path)


def format_toc_section(section_title: str, entries: list[tuple[int, str]]) -> list[str]:
    lines = [f"### {section_title}"]
    if not entries:
        lines.append("- _No recipes yet_")
        return lines

    for number, title in entries:
        lines.append(f"- [{number}. {title}](#{number}-{slugify(title)})")
    return lines


def build_book() -> str:
    sections = parse_index_sections(INDEX.read_text(encoding="utf-8"))
    recipes_by_section: list[tuple[str, list[tuple[int, str, str]]]] = []
    toc_sections: list[tuple[str, list[tuple[int, str]]]] = []

    recipe_number = 1
    for section in sections:
        title = str(section["title"])
        raw_paths = section["paths"]
        assert isinstance(raw_paths, list)

        section_recipes: list[tuple[int, str, str]] = []
        section_toc: list[tuple[int, str]] = []

        for path in raw_paths:
            assert isinstance(path, Path)
            recipe_title, body = read_recipe(path)
            section_recipes.append((recipe_number, recipe_title, body))
            section_toc.append((recipe_number, recipe_title))
            recipe_number += 1

        recipes_by_section.append((title, section_recipes))
        toc_sections.append((title, section_toc))

    total_recipes = sum(len(entries) for _, entries in recipes_by_section)

    lines = [
        f"# {BOOK_TITLE}",
        "",
        BOOK_DESCRIPTION,
        "",
        "## Overview",
        f"- Total recipes: **{total_recipes}**",
    ]

    for section_title, entries in toc_sections:
        lines.append(f"- {section_title}: **{len(entries)}**")

    lines.extend(
        [
            "",
            "## How to Use This Book",
            "- Add or update recipe files under `recipes/`.",
            "- Keep `RECIPE_INDEX.md` in sync with the recipes you want included.",
            "- Regenerate this book with `python3 scripts/generate_recipe_book.py`.",
            "",
            "## Table of Contents",
        ]
    )

    for section_title, entries in toc_sections:
        lines.extend(["", *format_toc_section(section_title, entries)])

    for section_title, entries in recipes_by_section:
        lines.extend(["", "---", "", f"## {section_title}"])
        if not entries:
            lines.extend(["", "_No recipes in this section yet._"])
            continue

        for number, title, body in entries:
            lines.extend(
                [
                    "",
                    f"### {number}. {title}",
                    body,
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    BOOK.write_text(build_book(), encoding="utf-8")


if __name__ == "__main__":
    main()
