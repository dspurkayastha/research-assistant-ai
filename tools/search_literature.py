#!/usr/bin/env python3
"""
search_literature.py - Search across PubMed, CrossRef, Semantic Scholar.
"""

import argparse, logging, sys, json
from pathlib import Path
import requests
from Bio import Entrez

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def search_pubmed(query, retmax, email):
    Entrez.email = email
    record = Entrez.read(Entrez.esearch(db="pubmed", term=query, retmax=retmax))
    results = []
    for pmid in record["IdList"]:
        txt = Entrez.efetch(db="pubmed", id=pmid, retmode="text", rettype="abstract").read()
        results.append({"source":"PubMed","id":pmid,"text":txt})
    return results

def search_crossref(query, retmax):
    resp = requests.get("https://api.crossref.org/works", params={"query.title": query, "rows": retmax})
    items = resp.json().get("message", {}).get("items", [])
    return [{"source":"CrossRef","id":item.get("DOI"),"title":item.get("title",[""])[0],"authors":[a.get("family") for a in item.get("author",[])],"published":item.get("published-print",{}).get("date-parts",[[None]])[0][0]} for item in items]

def search_semanticscholar(query, retmax):
    resp = requests.get("https://api.semanticscholar.org/graph/v1/paper/search", params={"query":query,"limit":retmax,"fields":"title,authors,year,abstract"})
    data = resp.json().get("data",[])
    return [{"source":"SemanticScholar","id":d.get("paperId"),"title":d.get("title"),"year":d.get("year"),"text":d.get("abstract")} for d in data]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--retmax", type=int, default=5)
    parser.add_argument("--email", required=True)
    parser.add_argument("--outdir", type=Path, default=Path("literature_output"))
    args = parser.parse_args()

    setup_logging()
    args.outdir.mkdir(exist_ok=True)
    results = []
    results.extend(search_pubmed(args.query, args.retmax, args.email))
    results.extend(search_crossref(args.query, args.retmax))
    results.extend(search_semanticscholar(args.query, args.retmax))

    with (args.outdir/"literature_results.json").open("w") as f:
        json.dump(results, f, indent=2)
    logging.info(f"Saved literature_results.json")
