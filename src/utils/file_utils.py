
import soundfile as sf

from pathlib import Path


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def save_metadata_csv(metadata, output_path):
    import pandas as pd

    df = pd.DataFrame(metadata)
    df.to_csv(output_path, index=False)

    return len(df)

def save_sample(
    audio_array, sample_rate, output_path, metadata_entry, metadata_list, is_augmented
):
    sf.write(output_path, audio_array, sample_rate, format="WAV")
    duration_sec = len(audio_array) / sample_rate
    metadata_entry = metadata_entry.copy()
    metadata_entry.update(
        {
            "audio_path": str(output_path.resolve()),
            "duration_sec": round(duration_sec, 2),
            "is_augmented": is_augmented,
        }
    )
    metadata_list.append(metadata_entry)