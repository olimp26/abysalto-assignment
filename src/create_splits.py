import os
import yaml
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

from utils.logger import get_logger
from utils.file_utils import create_dir

logger = get_logger(__name__)


def load_metadata(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Metadata file not found at {csv_path}")
    return pd.read_csv(csv_path)


def split_and_save(df, output_dir, test_size=0.1, val_size=0.1, random_state=42):
    create_dir(output_dir)

    train_val, test = train_test_split(
        df, test_size=test_size, random_state=random_state, stratify=df["language"]
    )
    train, val = train_test_split(
        train_val,
        test_size=val_size / (1 - test_size),
        random_state=random_state,
        stratify=train_val["language"],
    )

    for split_name, split_df in [("train", train), ("val", val), ("test", test)]:
        split_path = Path(output_dir) / f"{split_name}_manifest.csv"
        split_df.to_csv(split_path, index=False)
        logger.info(
            f"Saved {split_name} split to {split_path} — {len(split_df)} samples"
        )


def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    metadata_path = Path(config["output_dir"]) / "language_dialect_metadata.csv"

    logger.info(f"Loading metadata from: {metadata_path}")
    df = load_metadata(metadata_path)

    # Ensure required column exists
    if "is_augmented" not in df.columns:
        logger.warning(
            "'is_augmented' column missing in metadata — assuming all samples are original."
        )
        df["is_augmented"] = False

    output_dir = Path(config["output_dir"]) / "splits"
    split_and_save(
        df,
        output_dir,
        test_size=config.get("test_size", 0.1),
        val_size=config.get("val_size", 0.1),
    )


if __name__ == "__main__":
    main()
