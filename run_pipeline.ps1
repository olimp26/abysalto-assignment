& .\venv\Scripts\Activate.ps1

Write-Host "Starting download_data.py"
python src\download_data.py
Write-Host "Finished download_data.py"

Write-Host "Starting preprocess_audio.py"
python src\preprocess_audio.py
Write-Host "Finished preprocess_audio.py"

Write-Host "Starting create_splits.py"
python src\create_splits.py
Write-Host "Finished create_splits.py"

Write-Host "Starting quality_checks.py with metadata"
python src\quality_checks.py .\data\language_dialect_metadata.csv
Write-Host "Finished quality_checks.py"
