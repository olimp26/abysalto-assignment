import yaml

from datasets import load_dataset

from utils.logger import get_logger

logger = get_logger(__name__)


def main():

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    dataset_name = config["dataset_source"]
    languages = config["target_languages"]

    for lang in languages:
        try:
            logger.info(f"Downloading/loading from cache dataset for language: {lang}")
            load_dataset(dataset_name, lang, split="train")
            logger.info(f"Successfully downloaded/loaded from cache {lang}")
        except Exception as e:
            logger.error(f"Failed to download {lang}: {e}")


if __name__ == "__main__":
    main()
