#!/usr/bin/env python3
"""
generate_visuals.py - Boxplot, violin, pairplot, ROC.
"""

import argparse, logging, sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

sns.set_theme(style="whitegrid")
def setup_logging(): logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--group"); parser.add_argument("--value"); parser.add_argument("--score")
    parser.add_argument("--outdir", type=Path, default=Path("visuals_output"))
    args = parser.parse_args()
    setup_logging(); args.outdir.mkdir(exist_ok=True)
    df = pd.read_csv(args.csv)
    if args.group and args.value:
        sns.boxplot(data=df, x=args.group, y=args.value); plt.savefig(args.outdir/"boxplot.png"); plt.clf()
        sns.violinplot(data=df, x=args.group, y=args.value); plt.savefig(args.outdir/"violinplot.png"); plt.clf()
    sns.pairplot(df); plt.savefig(args.outdir/"pairplot.png"); plt.clf()
    if args.score:
        y=df[args.group or args.value]; s=df[args.score]; fpr,tpr,_=roc_curve(y,s); plt.plot(fpr,tpr,label=f"AUC={auc(fpr,tpr):.2f}"); plt.plot([0,1],[0,1],'--'); plt.legend(); plt.savefig(args.outdir/"roc_curve.png")
if __name__=="__main__":
    main()
