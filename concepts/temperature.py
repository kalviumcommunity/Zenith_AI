#!/usr/bin/env python3
"""
Temperature demo (standalone).

Purpose:
  Show how different temperature values affect creativity and variability in outputs.

Usage:
  export OPENAI_API_KEY=...           # required
  python temperature.py \
      --prompt "Write 2 lines about the benefits of unit tests" \
      --model gpt-4o-mini \
      --temperature 0.2

  # Sweep multiple temperatures
  python temperature.py \
      --prompt "A one-paragraph product description for a smart mug" \
      --sweep 0.0,0.3,0.7,1.0 \
      --model gpt-4o-mini

Notes:
- Higher temperature => more diverse and creative outputs, but potentially less factual/consistent.
- Lower temperature => more deterministic and conservative outputs.
"""
import os
import argparse
import sys
from typing import List


def parse_args():
    p = argparse.ArgumentParser(description="Temperature effect demo")
    p.add_argument(
        "--prompt",
        default=(
            "Write a short creative story about a time-traveling botanist who discovers a healing plant."
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
        help="Single temperature to use when --sweep is not set",
    )
    p.add_argument(
        "--sweep",
        default=None,
        help="Comma-separated temperatures to compare, e.g., '0.0,0.3,0.7,1.0'",
    )
    p.add_argument(
        "--n",
        type=int,
        default=1,
        help="Generate N outputs per temperature (>=1)",
    )
    return p.parse_args()


def parse_sweep(sweep_str: str) -> List[float]:
    vals: List[float] = []
    for chunk in sweep_str.split(","):
        s = chunk.strip()
        if not s:
            continue
        try:
            vals.append(float(s))
        except ValueError:
            raise SystemExit(f"Invalid temperature in --sweep: '{s}'")
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

    temps = parse_sweep(args.sweep) if args.sweep else [args.temperature]

    messages = [
        {"role": "system", "content": "You are a helpful, concise assistant."},
        {"role": "user", "content": args.prompt},
    ]

    for t in temps:
        print(f"\n=== Temperature: {t} ===\n")
        for i in range(args.n):
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    messages=messages,
                    temperature=t,
                )
            except Exception as e:
                print(f"Request failed at temperature {t}: {e}", file=sys.stderr)
                sys.exit(2)

            content = resp.choices[0].message.content
            if args.n > 1:
                print(f"-- Sample {i+1} --")
            print(content)
            if args.n > 1:
                print()


if __name__ == "__main__":
    main()