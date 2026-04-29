from __future__ import annotations

import argparse
from pathlib import Path

from jd_resume_agent.analyzer import analyze, to_markdown
from jd_resume_agent.parsers import load_inputs



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JD Resume Matching Agent")
    parser.add_argument("--resume", required=True, help="Path to resume file (.txt/.md/.docx)")
    parser.add_argument("--jd", required=True, help="Path to JD file (.txt/.md/.docx)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Optional output file path")
    return parser



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    payload = load_inputs(args.resume, args.jd)
    result = analyze(payload["resume_text"], payload["jd_text"])

    rendered = result.to_json() if args.format == "json" else to_markdown(result)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
