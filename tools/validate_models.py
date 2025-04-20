#!/usr/bin/env python3
"""
validate_models.py - K-fold CV and diagnostics.
"""

import argparse, logging, sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--predictors", required=True, nargs="+")
    parser.add_argument("--model", choices=["linear","logistic"], default="linear")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--outdir", type=Path, default=Path("validation_output"))
    args = parser.parse_args()

    setup_logging(); args.outdir.mkdir(exist_ok=True)
    df = pd.read_csv(args.csv)
    X = df[args.predictors].values; y = df[args.outcome].values
    kf = KFold(n_splits=args.folds, shuffle=True, random_state=42)
    if args.model=="linear":
        model = LinearRegression(); scoring="neg_mean_squared_error"
    else:
        model = LogisticRegression(max_iter=1000); scoring="accuracy"
    scores = cross_val_score(model, X, y, cv=kf, scoring=scoring)
    pd.DataFrame({f"fold{i+1}":[(-s)**0.5] if scoring.startswith("neg") else [s] for i,s in enumerate(scores)}).to_csv(args.outdir/"cv_results.csv", index=False)
    model.fit(X,y); preds = model.predict(X)
    plt.figure(); plt.scatter(y,preds); plt.savefig(args.outdir/"actual_vs_predicted.png")
    plt.figure(); vals = model.predict_proba(X)[:,1] if args.model=="logistic" else preds; plt.hist(vals, bins=10); plt.savefig(args.outdir/"predicted_dist.png")

if __name__=="__main__":
    main()
