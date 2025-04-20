#!/usr/bin/env python3
"""
write_paper.py - Draft manuscript and export to Markdown, PDF, LaTeX.
"""

import argparse, logging, sys
from pathlib import Path
import openai
import pypandoc

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def draft_markdown(data_text, lit_text, model):
    prompt = (f"Using this data:\n{data_text}\nAnd these literature summaries:\n{lit_text}"
              "\nWrite a full scientific manuscript with Abstract, Introduction, Methods, Results, Discussion.")
    resp = openai.ChatCompletion.create(model=model,messages=[{"role":"user","content":prompt}],temperature=0.2,max_tokens=3000)
    return resp.choices[0].message.content

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("data_insights", type=Path)
    parser.add_argument("lit_summary", type=Path)
    parser.add_argument("--model", default="gpt-4")
    parser.add_argument("--out", type=Path, default=Path("manuscript.md"))
    parser.add_argument("--to-pdf", type=Path)
    parser.add_argument("--to-tex", type=Path)
    args=parser.parse_args()

    setup_logging()
    openai.api_key=sys.getenv("OPENAI_API_KEY"); 
    if not openai.api_key: logging.error("API key not set"); sys.exit(1)
    data_text=args.data_insights.read_text(); lit_text=args.lit_summary.read_text()
    md = draft_markdown(data_text, lit_text, args.model)
    args.out.write_text(md); logging.info(f"Saved {args.out}")
    if args.to_pdf: pypandoc.convert_text(md,'pdf',format='md',outputfile=str(args.to_pdf)); logging.info(f"PDF: {args.to_pdf}")
    if args.to_tex: args.to_tex.write_text(pypandoc.convert_text(md,'latex',format='md')); logging.info(f"LaTeX: {args.to_tex}")
