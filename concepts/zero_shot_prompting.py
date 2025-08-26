#!/usr/bin/env python3
"""
Zero-shot prompting demo (standalone).

Purpose:
  Show a minimal prompt with no examples and get a helpful answer.

Usage:
  export OPENAI_API_KEY=...           # required
  python zero_shot_prompting.py \
      --instruction "Explain TCP vs UDP for a beginner" \
      --model gpt-4o-mini \
      --temperature 0.7

Notes:
- Only depends on the OpenAI Python SDK.
- Outputs plain text to stdout.
"""
import os
import argparse
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Zero-shot prompting CLI")
    p.add_argument(
        "--instruction",
        default="Write a friendly haiku about writing clean code.",
        help="Task/instruction for the model",
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
        help="Sampling temperature (0.0-2.0)",
    )
    return p.parse_args()


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
        {"role": "system", "content": "You are a concise, helpful assistant."},
        {"role": "user", "content": args.instruction},
    ]

    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
        )
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()