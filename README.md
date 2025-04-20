# Research Assistant AI Toolkit (Complete)

A comprehensive suite of production-ready CLI tools for scientific research workflows, including:

- PDF ingestion  
- Excel ingestion  
- Advanced data analysis (stats & modeling)  
- Model validation (cross-validation & diagnostics)  
- Data visualization  
- Literature search (PubMed, CrossRef, Semantic Scholar)  
- Manuscript drafting (Markdown, PDF, LaTeX)  
- Python code generation  

## Installation

1. Clone or download this repository.  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Repository Structure

```
research-assistant-ai-full/
├── .gitignore
├── README.md
├── codex.json
├── requirements.txt
└── tools/
    ├── analyze_advanced.py
    ├── generate_visuals.py
    ├── ingest_excel.py
    ├── ingest_pdf.py
    ├── search_literature.py
    ├── validate_models.py
    ├── write_code.py
    └── write_paper.py
```

## Usage Examples

```bash
# PDF ingestion
tools/ingest_pdf.py input.pdf --out extracted.txt --log pdf.log

# Excel ingestion
tools/ingest_excel.py data.xlsx --outdir excel_output

# Data analysis
tools/analyze_advanced.py data.csv --outcome outcome_col --predictors var1 var2 --event event_col

# Model validation
tools/validate_models.py data.csv --outcome outcome_col --predictors var1 var2 --model linear --folds 5

# Visualizations
tools/generate_visuals.py data.csv --group GroupVar --value OutcomeVar --score PredScore

# Literature search
tools/search_literature.py "thyroid carcinoma PD-L1" --email you@example.com --retmax 10

# Manuscript drafting
tools/write_paper.py analysis_output/descriptive_stats.csv literature_output/literature_results.json --model gpt-4 --out draft.md --to-pdf draft.pdf --to-tex draft.tex

# Python code generation
tools/write_code.py --prompt "Create a seaborn heatmap of correlation matrix" --outfile heatmap.py
```
