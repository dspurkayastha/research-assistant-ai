#!/usr/bin/env python3
"""
ingest_excel.py - Convert multi-sheet Excel to normalized CSVs.
"""

import argparse, logging, sys, re
from pathlib import Path
import pandas as pd

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def normalize(col):
    col = col.strip().lower()
    col = re.sub(r'\s+', '_', col)
    return re.sub(r'[^0-9a-z_]', '', col)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("excel", type=Path)
    parser.add_argument("--outdir", type=Path, default=Path("excel_output"))
    args = parser.parse_args()

    setup_logging()
    if not args.excel.exists():
        logging.error("Excel not found")
        sys.exit(1)
    args.outdir.mkdir(exist_ok=True)
    xls = pd.ExcelFile(args.excel)
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        df.columns = [normalize(c) for c in df.columns]
        out_path = args.outdir / f"{args.excel.stem}_{normalize(sheet)}.csv"
        df.to_csv(out_path, index=False)
        logging.info(f"Saved {out_path}")

if __name__=="__main__":
    main()
