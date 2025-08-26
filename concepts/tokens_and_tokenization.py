#!/usr/bin/env python3
"""
Tokens and tokenization demo (standalone, no API calls).

Purpose:
  Count approximate tokens for given text or a file using `tiktoken` if available,
  otherwise fall back to a simple heuristic.

Usage examples:
  python tokens_and_tokenization.py --text "Hello world"
  python tokens_and_tokenization.py --file ../Zenith_AI/Readme.md
  python tokens_and_tokenization.py --file some.txt --model gpt-4o-mini

Notes:
- No network access required.
- If `tiktoken` is installed, results are closer to true model tokenization.
  Install via: pip install tiktoken
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional


def get_encoding_name(model: str) -> str:
    """Map model name to a tiktoken encoding name.

    tiktoken encodings commonly used:
    - cl100k_base: Suitable for GPT-4/3.5 and many modern OpenAI models
    - o200k_base: For some newer Omni models (if supported by your tiktoken version)

    We default to cl100k_base for safety if the specific one isn't available.
    """
    m = model.lower()
    # Very simple mapping; adjust as needed
    if any(k in m for k in ["gpt-4", "gpt-3.5", "mini", "o1", "omni"]):
        return "cl100k_base"
    return "cl100k_base"


def count_tokens(text: str, model: str) -> int:
    """Count tokens using tiktoken when available; otherwise a rough heuristic.

    Heuristic: ~4 characters per token (English-centric).
    """
    try:
        import tiktoken  # type: ignore
        enc_name = get_encoding_name(model)
        enc = tiktoken.get_encoding(enc_name)
        return len(enc.encode(text))
    except Exception:
        return max(1, len(text) // 4)


def load_text(file: Optional[str], text: Optional[str]) -> str:
    if file:
        p = Path(file)
        if not p.exists():
            raise SystemExit(f"File not found: {file}")
        return p.read_text(encoding="utf-8", errors="ignore")
    return text or ""


def parse_args():
    p = argparse.ArgumentParser(description="Token counting utility")
    p.add_argument("--text", help="Inline text to count")
    p.add_argument("--file", help="Path to file whose content to count")
    p.add_argument("--model", default="gpt-4o-mini", help="Model name for tokenizer mapping")
    p.add_argument("--show-sample", type=int, default=0, help="Print first N characters of the input")
    return p.parse_args()


def main():
    args = parse_args()
    body = load_text(args.file, args.text)
    if not body:
        raise SystemExit("Provide --text or --file")

    n_tokens = count_tokens(body, args.model)

    if args.show_sample > 0:
        sample = body[: args.show_sample]
        print("=== Sample ===")
        print(sample)
        print("==============\n")

    print("Model:", args.model)
    print("Characters:", len(body))
    print("Approx tokens:", n_tokens)


if __name__ == "__main__":
    main()