import os
import sys
import pandas as pd
import yaml

from datasets import Dataset

from utils.logger import get_logger

logger = get_logger(__name__)


def export_manifest(df: pd.DataFrame, output_dir: str, formats=["csv", "json", "hf"]):
    if "csv" in formats:
        csv_path = f"./{output_dir}/manifest.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV manifest exported to {csv_path}")

    if "json" in formats:
        json_path = f"{output_dir}/manifest.json"
        df.to_json(json_path, orient="records", lines=True)
        logger.info(f"JSON manifest exported to {json_path}")

    if "hf" in formats:
        ds = Dataset.from_pandas(df)
        ds.save_to_disk(f"{output_dir}/hf_dataset")
        logger.info(f"HuggingFace dataset saved to {output_dir}/hf_dataset")


def main():
    config_paths = ["./config.yaml", "./src/config.yaml"]
    config_path = next((p for p in config_paths if os.path.exists(p)), None)
    if not config_path:
        logger.error("config.yaml not found in project root or src/")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    output_dir = config.get("output_dir", "data")
    formats = config.get("export_formats", ["csv"])

    metadata_csv = os.path.join(output_dir, "language_dialect_metadata.csv")
    if not os.path.exists(metadata_csv):
        logger.error(f"Metadata CSV not found at expected location: {metadata_csv}")
        sys.exit(1)

    df = pd.read_csv(metadata_csv)
    export_manifest(df, output_dir=output_dir, formats=formats)
    logger.info("Manifest export completed successfully.")


if __name__ == "__main__":
    main()
