import random
import torchaudio
import torch

from torchaudio.transforms import PitchShift


def apply_speed_perturbation(audio_tensor, sample_rate, factor_range=(0.9, 1.1)):
    factor = random.uniform(*factor_range)
    return torchaudio.functional.resample(
        audio_tensor, sample_rate, int(sample_rate * factor)
    )


def apply_pitch_shift(audio_tensor, sample_rate, n_steps_range=(-2, 2)):
    n_steps = random.randint(*n_steps_range)
    transform = PitchShift(sample_rate, n_steps=n_steps)
    return transform(audio_tensor)


def apply_background_noise(audio_tensor, noise_level=0.01):
    noise = torch.randn_like(audio_tensor) * noise_level
    return audio_tensor + noise


def augment_audio(audio_tensor, sample_rate, config):
    
    if config.get("enable_speed_perturbation", False):
        audio_tensor = apply_speed_perturbation(audio_tensor, sample_rate)

    if config.get("enable_pitch_shift", False):
        audio_tensor = apply_pitch_shift(audio_tensor, sample_rate)

    if config.get("enable_background_noise", False):
        audio_tensor = apply_background_noise(
            audio_tensor, config.get("background_noise_level", 0.01)
        )

    return audio_tensor
