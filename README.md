# Plagiarism Checker Pro - Complete Suite

A multi-mode plagiarism detection project with desktop UIs, CLI usage, batch processing, and report generation.

## Features

### Interfaces
- Basic GUI (`--mode basic`) for quick checks
- Advanced GUI (`--mode advanced`) with algorithm selection, database management, and batch tab
- Ultimate GUI (`--mode ultimate`) with extended analysis tools
- CLI mode (`--mode cli`) for scripting/automation
- Batch mode (`--mode batch`) for folder processing
- Server mode (`--mode server`) for a simple HTTP health endpoint

### Detection Engines
- `BasePlagiarismEngine`: cosine-based baseline checks
- `AdvancedPlagiarismEngine`: cosine, jaccard, n-gram, sequence, and stats
- `UltimatePlagiarismEngine`: extended algorithms and optional NLP/readability paths

### Reports
- Basic text reports
- Advanced text and HTML reports
- JSON report export
- PDF export when `reportlab` is installed

### Storage
- SQLite-backed reference document database
- Check history tracking
- Category organization for source documents

## Project Structure

Key entry points:
- `main.py` - main launcher and mode routing
- `run.bat` / `run.sh` - interactive startup scripts
- `core/` - engines, database, utilities, batch processor
- `ui/` - GUI and CLI interfaces
- `reports/` - report builders
- `api/` - lightweight server mode

## Requirements

- Python 3.8+
- Windows, Linux, or macOS

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional for PDF export:

```bash
pip install reportlab
```

## Running The App

### Option 1: Interactive Script (Recommended)

Windows:

```bat
run.bat
```

Linux/macOS:

```bash
chmod +x run.sh
./run.sh
```

Script menu provides:
1. Basic GUI
2. Advanced GUI
3. CLI
4. Batch

### Option 2: Direct Command Line

```bash
python main.py --mode basic
python main.py --mode advanced
python main.py --mode ultimate
python main.py --mode cli --document "path/to/file.txt"
python main.py --mode batch --input-dir "path/to/folder"
python main.py --mode server
```

Useful options:

```bash
python main.py --config config.json
python main.py --mode cli --document "essay.txt" --output "report.txt"
python main.py --mode batch --input-dir "docs" --output "exports/batch_reports"
```

## Batch Mode Behavior

- If `--input-dir` is omitted, batch mode defaults to `data/sample_documents`.
- If the folder does not exist or has no supported files, the app prints a message and exits cleanly.

## Supported Input Formats

Currently handled in processing paths:
- `.txt`
- `.docx`
- `.pdf`

Additional formats may appear in config and future handlers, but the active batch/CLI processing is primarily the three formats above.

## Quick Troubleshooting

- Import errors when running directly: launch through `main.py` from project root.
- GUI issues: ensure Tkinter is available in your Python install.
- PDF export failure: install `reportlab`.
- Empty batch results: verify your folder contains `.txt`, `.docx`, or `.pdf` files.

## Example Commands

```bash
python main.py --mode cli --document data/sample_documents/sample.txt
python main.py --mode batch --input-dir data/sample_documents --output exports/reports
python main.py --mode advanced
```