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

TODO:
Explain your decisions via code comments/docstrings and a README.md file.
Include:
• What data you selected and why
• Your dialect coverage
• Limitations of the dataset
• How your pipeline could scale to support 100+ dialects

I selected huggingface because it had a lot of examples and the downloading process was easy to do with "datasets". The languages i chose are small enough for a quick download and filter, and have multiple dialects (i checked using the dialect_check.py script).
Dor 6 languages i covered 14 total dialects. By updating config.yaml, its really easy to add language and dialect coverage. When the dataset is downloaded, it's filtered and for the accents available it takes 300 seconds of audio data (or as much as is available).

README.md with:
• Setup instructions (OK)
• Overview of your approach

My approach was using huggingface and datasets to download the dataset, then take as many sample audio files so that I have roughly 5 minutes per dialect (6 languages and 14 dialects). after downloading the data using data_download.py, the process_audio script:

Cleans metadata
Removes invalid/missing/empty samples
Converts all audio to consistent format (mono WAV, 16 kHz)
TODO: data augmentation
Saves all audio in the data/original_data folder ready for test/train/val splitting

Which is done by the create_splits script. quality_checks.py handles:
Prints basic dataset stats (number of samples, avg duration, distribution per dialect)
Plots duration histogram
Verifies label consistency and encoding

• Dataset description and statistics
Available on the release/data.dump branch, where i uploaded the data folder with everything.
• Optional improvements, if any
implement data augmentation and Spectrogram dashboard: Create a Streamlit or Jupyter-based mini-dashboard to browse spec
trograms and hear samples with their metadata.
