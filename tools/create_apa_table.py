#!/usr/bin/env python3
"""
create_apa_table.py - Generate an APA-style table from a CSV dataset.

Computes N, mean (M), and standard deviation (SD) for numeric columns
and outputs tables in Markdown and LaTeX formats.
"""

import argparse
import logging
import sys
from pathlib import Path
import pandas as pd

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def main():
    parser = argparse.ArgumentParser(description="Generate APA-style descriptive table")
    parser.add_argument("csv", type=Path, help="Input CSV file")
    parser.add_argument("--out", type=Path, default=Path("apa_table.md"), help="Output Markdown file")
    parser.add_argument("--to-tex", type=Path, help="Output LaTeX file")
    args = parser.parse_args()

    setup_logging()
    if not args.csv.exists():
        logging.error(f"CSV not found: {args.csv}")
        sys.exit(1)

    df = pd.read_csv(args.csv)
    numeric = df.select_dtypes(include='number').columns
    records = []
    for col in numeric:
        series = df[col].dropna()
        records.append({
            'Variable': col,
            'N': series.count(),
            'M': f"{series.mean():.2f}",
            'SD': f"{series.std():.2f}"
        })
    apa_df = pd.DataFrame(records)

    md = apa_df.to_markdown(index=False)
    args.out.write_text(md)
    logging.info(f"APA table saved to {args.out}")

    if args.to_tex:
        tex = apa_df.to_latex(index=False, caption="Descriptive Statistics", label="tab:descriptive", float_format="%.2f")
        args.to_tex.write_text(tex)
        logging.info(f"LaTeX table saved to {args.to_tex}")

if __name__ == "__main__":
    main()
