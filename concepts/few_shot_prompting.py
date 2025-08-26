#!/usr/bin/env python3
"""
Few-shot prompting demo (standalone).

Purpose:
  Demonstrate how providing a few input/output examples can guide model behavior
  compared to zero-shot prompting.

Usage:
  export OPENAI_API_KEY=...           # required
  python few_shot_prompting.py \
      --instruction "Generate a concise email subject (<=8 words)." \
      --input "Wanted to follow up on our Q3 pipeline in the CRM..." \
      --model gpt-4o-mini \
      --temperature 0.7

  # Use examples from a JSONL file (each line: {"user": "...", "assistant": "..."} or {"input": "...", "output": "..."})
  python few_shot_prompting.py \
      --instruction "Summarize in 1 sentence with key metrics." \
      --input "Quarterly results show 18% YoY growth..." \
      --examples-file path/to/examples.jsonl

Notes:
- Only depends on the OpenAI Python SDK.
- JSONL examples provide flexibility; keys can be (user/assistant) or (input/output).
"""
import os
import argparse
import sys
from typing import List, Dict


def default_examples() -> List[Dict[str, str]]:
    """Built-in example pairs for subject line generation."""
    return [
        {
            "user": (
                "Instruction: Generate a concise email subject (<=8 words).\n"
                "Input: The team offsite is next Friday; please fill out the dietary form by Wednesday."
            ),
            "assistant": "Team offsite: fill dietary form by Wed",
        },
        {
            "user": (
                "Instruction: Generate a concise email subject (<=8 words).\n"
                "Input: Thanks for your purchase—your package ships tomorrow with tracking."
            ),
            "assistant": "Your order ships tomorrow (tracking inside)",
        },
        {
            "user": (
                "Instruction: Generate a concise email subject (<=8 words).\n"
                "Input: Quick reminder: book your 1:1s for next week."
            ),
            "assistant": "Reminder: book next week’s 1:1s",
        },
    ]


def load_examples_jsonl(path: str, instruction: str) -> List[Dict[str, str]]:
    pairs: List[Dict[str, str]] = []
    import json

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "user" in obj and "assistant" in obj:
                pairs.append({"user": obj["user"], "assistant": obj["assistant"]})
            elif "input" in obj and "output" in obj:
                # Normalize into the same prompt format used above
                user_msg = f"Instruction: {instruction}\nInput: {obj['input']}"
                pairs.append({"user": user_msg, "assistant": obj["output"]})
            else:
                raise ValueError("Each JSONL line must have user/assistant or input/output keys")
    if not pairs:
        raise ValueError("No examples found in JSONL file")
    return pairs


def parse_args():
    p = argparse.ArgumentParser(description="Few-shot prompting CLI")
    p.add_argument(
        "--instruction",
        default="Generate a concise email subject (<=8 words).",
        help="High-level task instruction",
    )
    p.add_argument(
        "--input",
        default=(
            "Wanted to follow up on our Q3 pipeline in the CRM; please add opportunities by Friday."
        ),
        help="The new input to evaluate",
    )
    p.add_argument("--examples-file", help="Path to JSONL file with example pairs")
    p.add_argument("--model", default=os.getenv("MODEL", "gpt-4o-mini"))
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--show-prompt", action="store_true", help="Print the constructed messages")
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

    # Build messages with few-shot examples
    system_msg = {
        "role": "system",
        "content": (
            "You are a precise assistant. Follow the format implied by examples and adhere to the instruction."
        ),
    }

    try:
        examples = load_examples_jsonl(args.examples_file, args.instruction) if args.examples_file else default_examples()
    except Exception as e:
        print(f"Failed to load examples: {e}", file=sys.stderr)
        sys.exit(1)

    messages: List[Dict[str, str]] = [system_msg]
    # Add example pairs
    for ex in examples:
        messages.append({"role": "user", "content": ex["user"]})
        messages.append({"role": "assistant", "content": ex["assistant"]})

    # Add the new query
    user_query = f"Instruction: {args.instruction}\nInput: {args.input}"
    messages.append({"role": "user", "content": user_query})

    if args.show_prompt:
        print("=== Messages ===")
        for i, m in enumerate(messages, 1):
            print(f"[{i}] {m['role']}: {m['content']}")
        print("================\n")

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