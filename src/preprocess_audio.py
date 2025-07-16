import yaml
import torch
from datasets import load_dataset
from tqdm import tqdm
from pathlib import Path

from utils.logger import get_logger
from utils.audio_utils import resample_and_mono
from utils.dataset_utils import group_samples_by_accent, select_samples_for_duration
from utils.file_utils import create_dir, save_metadata_csv, save_sample
from data_augmentation import augment_audio

logger = get_logger(__name__)


def filter_and_save_language_subset(lang_code, output_dir, config):
    logger.info(f"Processing language: {lang_code}")

    try:
        dataset = load_dataset(config["dataset_source"], lang_code, split="train")
    except Exception as e:
        logger.error(f"Skipping {lang_code} due to error: {e}")
        return None

    # Filter invalid samples
    dataset = dataset.filter(
        lambda x: (x.get("audio") is not None and x.get("sentence") not in (None, ""))
    )

    accent_samples = group_samples_by_accent(dataset)

    selected_samples = select_samples_for_duration(
        accent_samples, config["target_duration_per_accent_sec"]
    )

    original_dir = Path(output_dir) / "original_data" / lang_code
    augmented_dir = Path(output_dir) / "aug_data" / lang_code
    create_dir(original_dir)
    create_dir(augmented_dir)

    metadata = []
    for i, sample in enumerate(tqdm(selected_samples, desc=f"Saving {lang_code}")):
        audio = sample["audio"]
        audio_array = audio["array"]
        sampling_rate = audio["sampling_rate"]

        # Resample and mono
        audio_array, target_sr = resample_and_mono(
            audio_array, sampling_rate, config["sample_rate"]
        )

        filename = f"{lang_code}_{i}.{config['audio_format']}"
        path_original = original_dir / filename
        path_augmented = augmented_dir / filename

        metadata_entry = {
            "text": sample.get("sentence", ""),
            "language": lang_code,
            "speaker_id": sample.get("client_id", ""),
            "accent": sample.get("accent") or f"{lang_code}_standard",
        }

        # Save original
        save_sample(
            audio_array,
            target_sr,
            path_original,
            metadata_entry,
            metadata,
            is_augmented=False,
        )

        # Save augmented
        # if config.get("enable_data_augmentation", False):
        #     audio_tensor = torch.tensor(audio_array).unsqueeze(0)
        #     augmented_audio = augment_audio(
        #         audio_tensor, target_sr, config.get("augmentation_params", {})
        #     )
        #     save_sample(
        #         augmented_audio,
        #         target_sr,
        #         path_augmented,
        #         metadata_entry,
        #         metadata,
        #         is_augmented=True,
        #     )

    return metadata


def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    output_dir = config["output_dir"]
    create_dir(output_dir)

    all_metadata = []

    for lang in config["target_languages"]:
        meta = filter_and_save_language_subset(lang, output_dir, config)
        if meta:
            all_metadata.extend(meta)

    df_length = save_metadata_csv(
        all_metadata, Path(output_dir) / "language_dialect_metadata.csv"
    )

    logger.info(f"Preprocessing done. Total samples: {df_length}")


if __name__ == "__main__":
    main()
