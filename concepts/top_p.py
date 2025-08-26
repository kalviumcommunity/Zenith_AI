#!/usr/bin/env python3
"""
Top P (nucleus sampling) demo (standalone).

Purpose:
  Show how different top_p values affect output diversity by limiting tokens to
  the smallest probability mass whose cumulative probability >= top_p.

Usage:
  export OPENAI_API_KEY=...           # required
  python top_p.py \
      --prompt "List three creative uses for a paperclip" \
      --model gpt-4o-mini \
      --top-p 0.7

  # Sweep multiple top_p values
  python top_p.py \
      --prompt "Write a short product blurb for a reusable water bottle" \
      --sweep 1.0,0.9,0.7,0.3 \
      --model gpt-4o-mini

Notes:
- Lower top_p focuses on the most probable tokens; higher values allow more variety.
- Keep temperature constant when comparing top_p to isolate its effect.
"""
import os
import argparse
import sys
from typing import List


def parse_args():
    p = argparse.ArgumentParser(description="Top P (nucleus sampling) demo")
    p.add_argument(
        "--prompt",
        default=(
            "Write a whimsical one-paragraph description of a lantern that stores memories."
        ),
        help="User prompt/instruction",
    )
    p.add_argument(
        "--model",
        default=os.getenv("MODEL", "gpt-4o-mini"),
        help="Model name (default: env MODEL or gpt-4o-mini)",
    )
    p.add_argument(
        "--top-p",
        type=float,
        default=1.0,
        dest="top_p",
        help="Single top_p to use when --sweep is not set (0.0-1.0)",
    )
    p.add_argument(
        "--sweep",
        default=None,
        help="Comma-separated top_p values to compare, e.g., '1.0,0.9,0.7,0.3'",
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature to keep constant across runs",
    )
    p.add_argument(
        "--n",
        type=int,
        default=1,
        help="Generate N outputs per top_p value (>=1)",
    )
    return p.parse_args()


def parse_sweep(sweep_str: str) -> List[float]:
    vals: List[float] = []
    for chunk in sweep_str.split(","):
        s = chunk.strip()
        if not s:
            continue
        try:
            v = float(s)
        except ValueError:
            raise SystemExit(f"Invalid top_p in --sweep: '{s}'")
        if not (0.0 <= v <= 1.0):
            raise SystemExit(f"top_p must be between 0.0 and 1.0, got: {v}")
        vals.append(v)
    if not vals:
        raise SystemExit("--sweep provided but empty after parsing")
    return vals


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

    p_vals = parse_sweep(args.sweep) if args.sweep else [args.top_p]

    messages = [
        {"role": "system", "content": "You are a helpful, concise assistant."},
        {"role": "user", "content": args.prompt},
    ]

    for p_val in p_vals:
        print(f"\n=== top_p: {p_val} (temperature={args.temperature}) ===\n")
        for i in range(args.n):
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    messages=messages,
                    temperature=args.temperature,
                    top_p=p_val,
                )
            except Exception as e:
                print(f"Request failed at top_p {p_val}: {e}", file=sys.stderr)
                sys.exit(2)

            content = resp.choices[0].message.content
            if args.n > 1:
                print(f"-- Sample {i+1} --")
            print(content)
            if args.n > 1:
                print()


if __name__ == "__main__":
    main()