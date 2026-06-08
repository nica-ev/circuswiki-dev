from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from dynamic.workflow import check_dynamic_pages, refresh_dynamic_pages, scan_dynamic_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="CircusWiki dynamic page tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="List dynamic pages")
    scan_parser.add_argument("--lang", default="")

    check_parser = subparsers.add_parser("check", help="Validate dynamic blocks")
    check_parser.add_argument("path", nargs="?")
    check_parser.add_argument("--lang", default="")

    preview_parser = subparsers.add_parser("preview", help="Render without writing")
    preview_parser.add_argument("path", nargs="?")
    preview_parser.add_argument("--lang", default="")

    refresh_parser = subparsers.add_parser("refresh", help="Render and write dynamic blocks")
    refresh_parser.add_argument("path", nargs="?")
    refresh_parser.add_argument("--lang", default="")
    refresh_parser.add_argument("--all", action="store_true", help="Refresh all matching pages")

    args = parser.parse_args()

    if args.command == "scan":
        print_json(scan_dynamic_pages(language=args.lang))
        return
    if args.command == "check":
        print_json(check_dynamic_pages(path=args.path or "", language=args.lang))
        return
    if args.command == "preview":
        print_json(refresh_dynamic_pages(path=args.path or "", language=args.lang, dry_run=True))
        return
    if args.command == "refresh":
        if not args.path and not args.all:
            parser.error("refresh requires a path or --all")
        print_json(refresh_dynamic_pages(path=args.path or "", language=args.lang, dry_run=False))
        return


def print_json(payload: Any) -> None:
    import json

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
