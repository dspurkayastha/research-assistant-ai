#!/usr/bin/env python3
"""
analyze_advanced.py - Descriptive, regression, survival analyses.
"""

import argparse, logging, sys
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
from lifelines import CoxPHFitter
from statsmodels.tools.sm_exceptions import PerfectSeparationError

def setup_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--predictors", required=True, nargs="+")
    parser.add_argument("--event", help="Event column for Cox", default=None)
    parser.add_argument("--outdir", type=Path, default=Path("analysis_output"))
    parser.add_argument("--log", type=Path, default=Path("analyze_advanced.log"))
    args = parser.parse_args()

    setup_logging(args.log)
    if not args.csv.exists():
        logging.error("CSV not found"); sys.exit(1)
    args.outdir.mkdir(exist_ok=True)

    df = pd.read_csv(args.csv)
    df.describe(include="all").to_csv(args.outdir / "descriptive_stats.csv")
    df.corr().to_csv(args.outdir / "correlation_matrix.csv")

    if args.event:
        data = df[[args.outcome, args.event] + args.predictors].dropna()
        cph = CoxPHFitter().fit(data, duration_col=args.outcome, event_col=args.event)
        cph.summary.to_csv(args.outdir / "cox_summary.csv")
    else:
        y = df[args.outcome]; X = sm.add_constant(df[args.predictors])
        if set(y.dropna().unique()) <= {0,1}:
            try:
                res = sm.Logit(y, X).fit(disp=False)
                (args.outdir / "logistic_summary.txt").write_text(res.summary().as_text())
            except PerfectSeparationError:
                logging.error("Perfect separation")
        else:
            res = sm.OLS(y, X).fit()
            (args.outdir / "linear_summary.txt").write_text(res.summary().as_text())

if __name__=="__main__":
    main()
