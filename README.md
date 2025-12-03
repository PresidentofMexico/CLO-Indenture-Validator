# CLO Compliance AI

Automated compliance checking for CLO (Collateralized Loan Obligation) documents using AI-powered analysis.

## Overview

This tool automates the validation of CLO indenture documents against compliance stipulations using:
- PDF document processing and section extraction
- AI-powered compliance evaluation via OpenAI's GPT models
- Automated report generation

## Project Structure

```
clo-compliance-ai/
├── config/
│   ├── __init__.py
│   └── settings.py          # Centralized Regex patterns (The "CLO Logic")
├── src/
│   ├── __init__.py
│   ├── document_processor.py # PDF Slicing & Section Extraction
│   ├── compliance_engine.py  # The LLM "Judge" (OpenAI integration)
│   └── data_loader.py        # Loading your Stips and Reports
├── input/                    # Placeholders for your PDF/Stips
│   └── README.md
├── output/                   # Where the Excel report lands
│   └── README.md
├── .env.example              # API Key template
├── .gitignore
├── requirements.txt
├── main.py                   # The Orchestrator
└── README.md
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PresidentofMexico/CLO-Indenture-Validator.git
   cd CLO-Indenture-Validator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Usage

### Run Compliance Check

```bash
python main.py --pdf input/indenture.pdf --stips input/stips.xlsx
```

### Extract Covenants

```bash
python main.py --pdf input/indenture.pdf --extract-covenants
```

### Prepare Your Input Files

1. **Place your CLO indenture PDF** in the `input/` directory
2. **Create a stipulations file** (Excel or CSV) with columns:
   - `id` - Unique identifier
   - `category` - Category (e.g., "Coverage Test")
   - `description` - The compliance rule to check
   - `section` - Document section (optional)

## Components

### Configuration (`config/settings.py`)
- Centralized regex patterns for document parsing
- Compliance thresholds and rules
- LLM prompt templates
- API configuration

### Document Processor (`src/document_processor.py`)
- PDF text extraction
- Section identification and extraction
- Pattern matching for key terms
- Table extraction

### Compliance Engine (`src/compliance_engine.py`)
- OpenAI GPT integration
- Compliance evaluation logic
- Covenant extraction
- Confidence scoring

### Data Loader (`src/data_loader.py`)
- Stipulations file loading
- Report generation and export
- Summary statistics
- File management

### Main Orchestrator (`main.py`)
- Workflow coordination
- Command-line interface
- Result aggregation

## Output

After running a compliance check, you'll find:
- `output/compliance_report.xlsx` - Detailed compliance report
- Summary statistics in console output
- Pass/Fail/Unclear status for each stipulation

## Requirements

See `requirements.txt` for full list of dependencies:
- Python 3.8+
- PyPDF2 / pdfplumber for PDF processing
- pandas / openpyxl for data handling
- openai for AI integration

## License

See LICENSE file for details.