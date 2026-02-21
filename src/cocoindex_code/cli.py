"""CLI for codebase indexing and querying."""

import argparse
import asyncio
import json
import sqlite3
import sys

from .indexer import app as indexer_app
from .query import query_codebase
from .shared import config


async def _async_index() -> None:
    """Async entry point for the index command."""
    await indexer_app.update(report_to_stdout=True)
    _print_index_stats()


async def _async_search(
    query: str,
    limit: int = 10,
    offset: int = 0,
    refresh_index: bool = True,
    output_json: bool = False,
) -> None:
    """Async entry point for the search command."""
    try:
        if refresh_index:
            await indexer_app.update(report_to_stdout=False)

        results = await query_codebase(query=query, limit=limit, offset=offset)

        if output_json:
            data = [
                {
                    "file_path": r.file_path,
                    "language": r.language,
                    "content": r.content,
                    "start_line": r.start_line,
                    "end_line": r.end_line,
                    "score": r.score,
                }
                for r in results
            ]
            print(json.dumps(data, indent=2))
        else:
            if not results:
                print("No results found.")
                return

            for i, r in enumerate(results):
                print(f"\n{'='*60}")
                print(f"Result {i + offset + 1} | Score: {r.score:.4f}")
                print(f"File: {r.file_path} ({r.language})")
                print(f"Lines: {r.start_line}-{r.end_line}")
                print(f"{'-'*60}")
                print(r.content)

            print(f"\n{'='*60}")
            print(f"Returned {len(results)} result(s) (offset: {offset})")

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Search failed: {e}", file=sys.stderr)
        sys.exit(1)


def _print_index_stats() -> None:
    """Print index statistics from the database."""
    db_path = config.target_sqlite_db_path
    if not db_path.exists():
        print("No index database found.")
        return

    conn = sqlite3.connect(str(db_path))
    try:
        total_chunks = conn.execute("SELECT COUNT(*) FROM code_chunks").fetchone()[0]
        total_files = conn.execute("SELECT COUNT(DISTINCT file_path) FROM code_chunks").fetchone()[
            0
        ]
        langs = conn.execute(
            "SELECT language, COUNT(*) as cnt FROM code_chunks GROUP BY language ORDER BY cnt DESC"
        ).fetchall()

        print("\nIndex stats:")
        print(f"  Chunks: {total_chunks}")
        print(f"  Files:  {total_files}")
        if langs:
            print("  Languages:")
            for lang, count in langs:
                print(f"    {lang}: {count} chunks")
    finally:
        conn.close()


def main() -> None:
    """Entry point for the cocoindex-code CLI."""
    parser = argparse.ArgumentParser(
        prog="cocoindex-code",
        description="CLI tool for indexing and querying codebases using CocoIndex.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # index subcommand
    subparsers.add_parser("index", help="Build/refresh the index and report stats")

    # search subcommand
    search_parser = subparsers.add_parser(
        "search", help="Search the codebase using semantic similarity"
    )
    search_parser.add_argument("query", help="Natural language query or code snippet to search for")
    search_parser.add_argument(
        "-l", "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return (1-100, default: 10)",
    )
    search_parser.add_argument(
        "-o", "--offset",
        type=int,
        default=0,
        help="Number of results to skip for pagination (default: 0)",
    )
    search_parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Skip index refresh before searching (faster for consecutive queries)",
    )
    search_parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output results in JSON format",
    )

    args = parser.parse_args()

    if args.command == "index":
        asyncio.run(_async_index())
    elif args.command == "search":
        asyncio.run(
            _async_search(
                query=args.query,
                limit=args.limit,
                offset=args.offset,
                refresh_index=not args.no_refresh,
                output_json=args.output_json,
            )
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
