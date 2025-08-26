#!/usr/bin/env python3
"""
Stop sequences demo (standalone).

Purpose:
  Show how stop sequences can be used to control where the model should stop generating.

Usage:
  export OPENAI_API_KEY=...           # required
  python stop_sequences.py \
      --prompt "Write a JSON object with keys title, summary, and notes." \
      --stop "\n\n" \
      --model gpt-4o-mini

  # Multiple stop sequences (comma-separated)
  python stop_sequences.py \
      --prompt "Give an outline: A), B), C) with subpoints." \
      --stop ")\n,\n\n" \
      --model gpt-4o-mini

Notes:
- When a stop sequence is encountered, generation ends and the sequence is not included in the output.
- Combine with max_tokens to set a hard cap as a backup.
"""
import os
import argparse
import sys
from typing import List


def parse_args():
    p = argparse.ArgumentParser(description="Stop sequences demo")
    p.add_argument(
        "--prompt",
        default=(
            "Write a brief product spec with sections: Title, Summary, Details."
        ),
        help="User prompt/instruction",
    )
    p.add_argument(
        "--model",
        default=os.getenv("MODEL", "gpt-4o-mini"),
        help="Model name (default: env MODEL or gpt-4o-mini)",
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature",
    )
    p.add_argument(
        "--stop",
        default=None,
        help="Comma-separated list of stop sequences (e.g., ")\n,\n\n")",
    )
    p.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        dest="max_tokens",
        help="Optional hard cap on tokens to generate",
    )
    p.add_argument("--show-prompt", action="store_true", help="Print the constructed messages")
    return p.parse_args()


def parse_stops(stop_str: str | None) -> List[str] | None:
    if not stop_str:
        return None
    parts = [s for s in (x.strip() for x in stop_str.split(",")) if s]
    return parts or None


def main():
    args = parse_args()

    try:
        from openai import OpenAI
    except Exception:
        print("Error: openai package not found. Install with: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set OPENAI_API_KEY in your environment.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": "You are a helpful, concise assistant."},
        {"role": "user", "content": args.prompt},
    ]

    stops = parse_stops(args.stop)

    if args.show_prompt:
        print("=== Messages ===")
        for i, m in enumerate(messages, 1):
            print(f"[{i}] {m['role']}: {m['content']}")
        print("Stops:", stops)
        print("================\n")

    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            stop=stops,
            max_tokens=args.max_tokens,
        )
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(2)

    choice = resp.choices[0]
    print(choice.message.content)
    if hasattr(choice, "finish_reason"):
        print(f"\n[finish_reason: {choice.finish_reason}]")


if __name__ == "__main__":
    main()