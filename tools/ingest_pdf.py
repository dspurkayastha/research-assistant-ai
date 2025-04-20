#!/usr/bin/env python3
"""
ingest_pdf.py - Extract text from PDF files using PyMuPDF.
"""

import argparse, logging, sys
from pathlib import Path
import fitz  # PyMuPDF

def setup_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
    )

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, default=Path("extracted_text.txt"))
    parser.add_argument("--log", type=Path, default=Path("ingest_pdf.log"))
    args = parser.parse_args()

    setup_logging(args.log)
    if not args.pdf.exists():
        logging.error("PDF not found")
        sys.exit(1)
    text = extract_text(args.pdf)
    args.out.write_text(text, encoding="utf-8")
    logging.info(f"Text extracted to {args.out}")

if __name__=="__main__":
    main()
