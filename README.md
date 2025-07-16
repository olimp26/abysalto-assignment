# Abysalto Speech Dataset Pipeline

## Overview

This project provides a complete pipeline for processing multilingual speech data from [Common Voice 17.0](https://commonvoice.mozilla.org/en/datasets), focusing on dialect and accent classification. It includes scripts for downloading, preprocessing, filtering, quality checking, and exporting structured metadata. The pipeline is designed to be modular, reproducible, and easily extensible to more languages and dialects.

---

## Setup Instructions

1. **Create and activate a virtual environment:**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the pipeline (Windows):**

```bash
./run_pipeline.ps1
```

> On Linux, run the scripts in sequence:
>
> - `download_data.py`
> - `preprocess_audio.py`
> - `create_splits.py`
> - `quality_check.py`
> - `export_manifest.py`

---

## Dataset Description

- **Source:** Common Voice 17.0
- **Languages Selected:** `af`, `da`, `ast`, `te`, `mk`, `ml`
- **Dialect Coverage:** 14 dialects across 6 languages
- **Audio Format:** WAV
- **Sample Rate:** 16kHz
- **Channels:** Mono
- **Clip Duration:** 1 to 15 seconds
- **Target Duration per Dialect:** ~300 seconds (or as much as available)

Each language's dataset includes:

- Original and (planned) augmented samples in separate folders
- Cleaned metadata in `data/language_dialect_metadata.csv`:
  - File path
  - Duration
  - Dialect label
  - Augmentation flag

> ⚠️ **Note:** Data augmentation is partially implemented but currently disabled due to unresolved bugs.

---

## Pipeline Stages

1. **Data Download (`download_data.py`)**  
   Uses Hugging Face’s `datasets` library to download filtered speech data for the selected languages and dialects, based on `config.yaml`.

2. **Audio Preprocessing (`preprocess_audio.py`)**

   - Cleans and validates metadata
   - Removes invalid, empty, or corrupted samples
   - Converts all audio to mono WAV format at 16kHz
   - Saves cleaned audio to `data/original_data/`
   - Ensures dialect-balanced splits

3. **Train/Val/Test Splitting (`create_splits.py`)**

   - Splits dataset into training, validation, and test sets
   - 80% train, 10% val and 10% test

4. **Quality Checks (`quality_check.py`)**

   - Prints dataset stats (e.g., number of samples, average duration)
   - Verifies label consistency and encoding
   - Plots duration histograms
   - Flags anomalies or inconsistencies

5. **Manifest Generation (`export_manifest.py`)**
   - Allow exporting the dataset manifest in multiple formats (CSV, JSON, HF compatible Dataset, etc.)

---

## Design Decisions

- **Why Common Voice via Hugging Face?**  
  Hugging Face's `datasets` library provides streamlined access to Common Voice and flexible filtering by language and accent.

- **Language Selection Criteria:**  
  Selected for small dataset sizes (to support quick development) and confirmed dialect diversity (using `dialect_check.py`).

- **Target Duration:**  
  ~5 minutes (300 seconds) per dialect to ensure balanced representation across languages.

---

## Limitations

- Data augmentation is not finalized and currently disabled
- Not all dialects have full 300s coverage due to data scarcity
- Only a subset of available languages are supported in this iteration
- Common Voice labels may vary in consistency across languages

---

## Scalability

The pipeline is built to scale:

- **Adding Languages/Dialects:**  
  Easily configured via `config.yaml`
- **Modular Scripts:**  
  Each stage is standalone and can be parallelized
- **Future Improvements:**
  - Add batching, caching, and multiprocessing
  - Transition to cloud storage for large datasets

---

## Future Improvements

- Finalize and integrate audio augmentation module
- Add a **Streamlit** or **Jupyter** dashboard to:
  - Display spectrograms
  - Play audio samples
  - Show associated metadata
- Extend coverage to additional Common Voice languages
- Include speaker-level metadata for advanced modeling

---

## Acknowledgments

This project uses Mozilla’s Common Voice dataset and Hugging Face’s `datasets` library.  
Large Language Model (LLM) assistance from OpenAI’s ChatGPT was used for:

- Debugging and fixing Python/audio issues
- Planning the pipeline architecture
- Suggesting improvements to code structure and YAML configuration
- Drafting augmentation logic
- Helping structure this README.md file

---
