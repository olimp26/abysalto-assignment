from collections import defaultdict


def group_samples_by_accent(dataset, default_accent="standard"):
    accent_buckets = defaultdict(list)
    for sample in dataset:
        accent = sample.get("accent") or default_accent
        accent_buckets[accent].append(sample)
    return accent_buckets


def select_samples_for_duration(accent_samples, target_duration_sec):
    from random import shuffle

    selected_samples = []
    for accent, samples in accent_samples.items():
        shuffle(samples)
        accumulated = 0
        for sample in samples:
            audio = sample["audio"]
            duration = len(audio["array"]) / audio["sampling_rate"]
            if accumulated >= target_duration_sec:
                break
            selected_samples.append(sample)
            accumulated += duration
    return selected_samples
