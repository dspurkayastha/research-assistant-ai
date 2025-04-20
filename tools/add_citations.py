#!/usr/bin/env python3
"""
add_citations.py - Insert inline citations into a document in a specified style.

Reads a text file and a references file (e.g., BibTeX), calls OpenAI to
insert inline citations in the desired style.
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

def read_file(path: Path) -> str:
    return path.read_text(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Insert inline citations into document")
    parser.add_argument("document", type=Path, help="Text document file")
    parser.add_argument("--style", choices=["apa","vancouver","mla"], default="apa", help="Citation style")
    parser.add_argument("--references", type=Path, required=True, help="References file (e.g. .bib)")
    parser.add_argument("--out", type=Path, default=Path("document_cited.txt"), help="Output file")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model ID")
    args = parser.parse_args()

    setup_logging()
    openai.api_key = sys.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        logging.error("OPENAI_API_KEY not set")
        sys.exit(1)

    doc_text = read_file(args.document)
    ref_text = read_file(args.references)

    prompt = (
        f"Insert inline citations into the following document using {args.style.upper()} style.\n\n"
        f"Document:\n{doc_text}\n\nReferences (BibTeX):\n{ref_text}"
    )

    response = openai.ChatCompletion.create(
        model=args.model,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens=3000
    )

    cited = response.choices[0].message.content
    args.out.write_text(cited)
    logging.info(f"Cited document saved to {args.out}")

if __name__ == "__main__":
    main()
