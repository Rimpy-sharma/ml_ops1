PDF to Markdown converter

This small utility extracts text and images from a PDF and writes a Markdown file.

Requirements



Usage

```powershell
# Basic: writes output next to the PDF
python pdf_to_md.py "C:\\Users\\Rimpy\\OneDrive\\Desktop\\ml _ops\\MLOp_Assignment_1.pdf"

# Specify output md and images directory
python pdf_to_md.py "C:\\path\\to\\input.pdf" "C:\\path\\to\\output.md" --images-dir "C:\\path\\to\\images"
```

Notes

- The script will create an images directory (default: `<output_basename>_images`) and save any embedded images there. The Markdown will reference the images using relative paths.
- PyMuPDF (fitz) provides much better extraction for images and layout than some pure-Python parsers.
````markdown
# ML Ops Assignment 1 - Boston Housing

This folder contains the solution for Assignment 1: training classical ML models
on a reconstructed Boston Housing dataset. The repo includes two training scripts
(`assignment _1/train.py` for DecisionTree and `assignment _1/train2.py` for KernelRidge),
shared utility functions (`assignment _1/misc.py`), and a GitHub Actions workflow
that runs both training scripts on pushes to the `kernelridge` branch.

## Install and run

Requirements: Python 3.8+ and pip.

Install dependencies from repository root (PowerShell):

```powershell
python -m pip install --upgrade pip; pip install -r "assignment _1/requirements.txt"
```

Run the DecisionTree training:

```powershell
python "assignment _1/train.py"
```

Run the KernelRidge training:

```powershell
python "assignment _1/train2.py"
```

## Repository branches (required for submission)

- `main` : README and report
- `dtree` : contains `assignment _1/train.py` and `assignment _1/misc.py`
- `kernelridge` : contains `assignment _1/train2.py` and `.github/workflows/ci.yml`

For the CI logs and screenshots required in the report, push your branches to GitHub
and capture the Actions run for the `kernelridge` branch.
````
