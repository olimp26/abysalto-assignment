import sys
import os
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore
import chardet  # type: ignore

from collections import Counter

from utils.logger import get_logger

logger = get_logger(__name__)


def print_basic_stats(df: pd.DataFrame):
    total_samples = len(df)
    avg_duration = df["duration_sec"].mean()
    accent_distribution = Counter(df["accent"])
    language_distribution = Counter(df["language"])

    logger.info(f"Total samples: {total_samples}")
    logger.info(f"Average duration (sec): {avg_duration:.2f}")
    logger.info(f"Accent distribution: {dict(accent_distribution)}")
    logger.info(f"Language distribution: {dict(language_distribution)}")

    print_total_duration_per_accent(df)


def print_total_duration_per_accent(df: pd.DataFrame):
    logger.info("Total duration per accent (in seconds):")
    grouped = df.groupby("accent")["duration_sec"].sum().round(2)
    for accent, total in grouped.items():
        logger.info(f"  {accent}: {total} sec")


def plot_duration_histogram(
    df: pd.DataFrame, output_path="./data/duration_histogram.png"
):
    plt.figure(figsize=(10, 6))
    plt.hist(df["duration_sec"], bins=50, color="skyblue", edgecolor="black")
    plt.title("Histogram of Clip Durations")
    plt.xlabel("Duration (sec)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Duration histogram saved to {output_path}")


def plot_total_duration_per_accent(
    df: pd.DataFrame, output_path="./data/total_duration_per_accent.png"
):
    total_per_accent = (
        df.groupby("accent")["duration_sec"].sum().sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))
    total_per_accent.plot(kind="bar", color="mediumpurple", edgecolor="black")
    plt.title("Total Clip Duration per Accent")
    plt.xlabel("Accent")
    plt.ylabel("Total Duration (sec)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Total duration per accent plot saved to {output_path}")


def verify_label_encoding(metadata_path: str):
    with open(metadata_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]

    logger.info(f"Detected file encoding: {encoding}")

    if encoding.lower() not in ["utf-8", "utf-8-sig"]:
        logger.warning("Detected non-UTF-8 encoding. Consider re-saving as UTF-8.")

    # Check for nulls or strange label formats
    df = pd.read_csv(metadata_path, encoding=encoding)
    null_counts = df[["accent", "language", "text"]].isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values detected in labels:\n{null_counts}")
    else:
        logger.info("No nulls found in label columns.")

    return df


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python quality_checks.py <metadata_csv>")
        sys.exit(1)

    metadata_csv = sys.argv[1]

    if not os.path.exists(metadata_csv):
        logger.error(f"Metadata CSV file does not exist: {metadata_csv}")
        sys.exit(1)

    df = verify_label_encoding(metadata_csv)
    print_basic_stats(df)
    plot_duration_histogram(df)
    plot_total_duration_per_accent(df)
    logger.info("Quality checks completed successfully.")
