# Abysalto Speech Dataset Pipeline

## Overview

This project processes multilingual speech data from Common Voice for accent classification and related tasks. It includes preprocessing, filtering, augmentation, and metadata generation steps.

---

## Setup Instructions

1. Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the run_pipeline.ps1 script # On Windows, on linux you can run in order: download_data.py, preprocess_audio.py, create_splits.py, quality_check.py and export_manifest.py

```bash
./run_pipeline.ps1
```

Dataset Description
Source: Common Voice 17.0

Languages i chose with a few accents and not that many rows: af, da, ast, te, mk, ml

Format: wav

Sample rate: 16kHz

Channels: Mono

Duration constraints: 1s – 15s

Target total duration per accent: 300s

For each language:

Original and augmented samples are stored separately

Metadata includes duration, augmentation flag, and path

(See data/language_dialect_metadata.csv after running the pipeline.)

IMPORTANT: data augmentation was only tried, in the end not fully implemented. Needs some more debugging

---

LLM assistance via ChatGPT (OpenAI) was used for:

Debugging errors (e.g., resolving soundfile and tensor issues)

Suggesting code structure improvements

Syntax correction and YAML configuration

Planning and partially implementing audio augmentation logic
