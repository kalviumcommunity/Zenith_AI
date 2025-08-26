#!/usr/bin/env python3
"""
Dynamic prompting demo (standalone).

Purpose:
  Show how to build prompts dynamically from variables like role, task, style, and constraints.

Usage:
  export OPENAI_API_KEY=...           # required
  python dynamic_prompting.py \
      --role "senior backend engineer" \
      --task "design a rate limiter" \
      --style "bullet points" \
      --constraints "give pros/cons and a quick summary" \
      --model gpt-4o-mini \
      --temperature 0.6

Notes:
- Only depends on the OpenAI Python SDK.
- Outputs plain text to stdout.
"""
import os
import argparse
import sys


def build_prompt(role: str, task: str, style: str, constraints: str) -> str:
    """Create a simple, readable dynamic prompt from user inputs."""
    lines = [
        f"You are a {role}.",
        f"Task: {task}.",
        f"Write the answer in {style}.",
        f"Constraints: {constraints}.",
        "Be clear, actionable, and concise.",
    ]
    return "\n".join(lines)


def parse_args():
    p = argparse.ArgumentParser(description="Dynamic prompting CLI")
    p.add_argument("--role", default="productivity coach", help="Persona for the assistant")
    p.add_argument("--task", default="create a morning routine for a student", help="Task to perform")
    p.add_argument("--style", default="numbered steps", help="Output style (e.g., bullet points)")
    p.add_argument(
        "--constraints",
        default="limit to 5 steps; include timing; mention breaks",
        help="Extra constraints",
    )
    p.add_argument("--model", default=os.getenv("MODEL", "gpt-4o-mini"))
    p.add_argument("--temperature", type=float, default=0.6)
    p.add_argument("--show-prompt", action="store_true", help="Print the built prompt before sending")
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

    user_prompt = build_prompt(args.role, args.task, args.style, args.constraints)
    if args.show_prompt:
        print("=== Built Prompt ===\n" + user_prompt + "\n====================\n")

    messages = [
        {"role": "system", "content": "You craft actionable, concise plans."},
        {"role": "user", "content": user_prompt},
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