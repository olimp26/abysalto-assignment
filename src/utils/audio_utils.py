import torch
import torchaudio


def resample_and_mono(audio_array, orig_sr, target_sr=16000):
    waveform = torchaudio.functional.resample(
        torch.tensor(audio_array).float().unsqueeze(0),
        orig_freq=orig_sr,
        new_freq=target_sr,
    )
    mono = waveform.mean(dim=0)  # convert to mono
    return mono.numpy(), target_sr
