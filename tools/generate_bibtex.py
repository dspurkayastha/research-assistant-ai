#!/usr/bin/env python3
"""
generate_bibtex.py

Fetches BibTeX entries for a list of identifiers (DOIs or PMIDs) and writes them
to a .bib file. PMIDs are resolved via CrossRef’s PMID filter.

Usage:
    python3 tools/generate_bibtex.py 10.1038/nature12373 31452104 \
        --out references.bib

Requirements:
    pip install requests
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import requests

CROSSREF_WORKS_URL = "https://api.crossref.org/works"
DOI_RESOLVE_URL = "https://doi.org/"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def fetch_bibtex_from_doi(doi: str, timeout: float = 10.0) -> str:
    """Fetch a BibTeX entry directly via DOI resolution."""
    headers = {"Accept": "application/x-bibtex"}
    url = DOI_RESOLVE_URL + doi
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text.strip()

def fetch_bibtex_from_pmid(pmid: str, timeout: float = 10.0) -> str:
    """
    Resolve a PMID to a DOI via CrossRef, then fetch the BibTeX.
    Returns empty string if not found.
    """
    params = {"filter": f"pmid:{pmid}", "rows": 1}
    resp = requests.get(CROSSREF_WORKS_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json().get("message", {}).get("items", [])
    if not data:
        logging.warning(f"No CrossRef entry found for PMID {pmid}")
        return ""
    doi = data[0].get("DOI")
    if not doi:
        logging.warning(f"No DOI in CrossRef record for PMID {pmid}")
        return ""
    return fetch_bibtex_from_doi(doi, timeout=timeout)

def is_pmid(identifier: str) -> bool:
    """Detect if the identifier is a numeric PMID."""
    return bool(re.fullmatch(r"\d+", identifier))

def main():
    parser = argparse.ArgumentParser(
        description="Generate a BibTeX file from DOIs or PMIDs"
    )
    parser.add_argument(
        "ids", nargs="+",
        help="List of DOIs (e.g. 10.1000/xyz123) or PMIDs (numeric)"
    )
    parser.add_argument(
        "--out", type=Path, default=Path("references.bib"),
        help="Output BibTeX file path"
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0,
        help="Network timeout in seconds"
    )
    args = parser.parse_args()

    setup_logging()
    entries = []

    for identifier in args.ids:
        try:
            if is_pmid(identifier):
                logging.info(f"Fetching BibTeX for PMID {identifier}")
                bib = fetch_bibtex_from_pmid(identifier, timeout=args.timeout)
            else:
                logging.info(f"Fetching BibTeX for DOI {identifier}")
                bib = fetch_bibtex_from_doi(identifier, timeout=args.timeout)
            if bib:
                entries.append(bib)
            else:
                logging.error(f"No BibTeX entry found for {identifier}")
        except requests.HTTPError as e:
            logging.error(f"HTTP error for {identifier}: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error fetching {identifier}")

    if not entries:
        logging.error("No entries fetched; exiting without writing file.")
        sys.exit(1)

    # Write out the .bib file
    content = "\n\n".join(entries) + "\n"
    args.out.write_text(content, encoding="utf-8")
    logging.info(f"Wrote {len(entries)} entries to {args.out}")

if __name__ == "__main__":
    main()
