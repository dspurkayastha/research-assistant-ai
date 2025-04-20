#!/usr/bin/env python3
"""
write_code.py - Generate custom Python code via OpenAI GPT.
Updated to use a system role and avoid default examples.
"""

import argparse
import logging
import sys
from pathlib import Path
import openai

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def generate_code(prompt, model):
    system_msg = (
        "You are an expert Python developer. "
        "Generate Python code exactly matching the user's request without additional examples or commentary."
    )
    user_msg = f"Please write Python code for the following request:\n{prompt}"
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0,
        max_tokens=1500
    )
    return resp.choices[0].message.content.strip()

def main():
    parser = argparse.ArgumentParser(description="Generate Python code from prompt")
    parser.add_argument("--prompt", required=True, help="Description of desired Python code")
    parser.add_argument("--outfile", type=Path, required=True, help="Path to save generated code")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model ID")
    args = parser.parse_args()

    setup_logging()
    openai.api_key = sys.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        logging.error("OPENAI_API_KEY not set")
        sys.exit(1)

    code = generate_code(args.prompt, args.model)
    args.outfile.write_text(code)
    logging.info(f"Generated code saved to {args.outfile}")

if __name__ == "__main__":
    main()
