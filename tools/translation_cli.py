from __future__ import annotations

import argparse
import json

from translation.workflow import health_summary, inspect_page, translate_page


def main() -> None:
    parser = argparse.ArgumentParser(description="CircusWiki translation workflow")
    subcommands = parser.add_subparsers(dest="command", required=True)

    health_parser = subcommands.add_parser("health", help="Inspect all source pages")
    health_parser.add_argument("--source-lang", default="de")
    health_parser.add_argument("--target-lang", default="en")

    inspect_parser = subcommands.add_parser("inspect", help="Inspect one source page")
    inspect_parser.add_argument("path")
    inspect_parser.add_argument("--source-lang", default="de")
    inspect_parser.add_argument("--target-lang", default="en")

    translate_parser = subcommands.add_parser("translate", help="Translate one source page")
    translate_parser.add_argument("path")
    translate_parser.add_argument("--source-lang", default="de")
    translate_parser.add_argument("--target-lang", default="en")
    translate_parser.add_argument("--model")
    translate_parser.add_argument("--prompt")
    translate_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.command == "health":
        print(json.dumps(health_summary(args.source_lang, args.target_lang), ensure_ascii=False, indent=2))
        return

    if args.command == "inspect":
        print(
            json.dumps(
                inspect_page(args.path, args.source_lang, args.target_lang).__dict__,
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "translate":
        print(
            json.dumps(
                translate_page(
                    source_path=args.path,
                    source_lang=args.source_lang,
                    target_lang=args.target_lang,
                    model=args.model,
                    prompt=args.prompt,
                    dry_run=args.dry_run,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
