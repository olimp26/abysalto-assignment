import requests
import time
import csv

HF_TOKEN = "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"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


# Step 1: Get list of language codes
def get_language_codes():
    url = "https://huggingface.co/api/datasets/mozilla-foundation/common_voice_17_0"
    return sorted(requests.get(url).json()["cardData"]["language"])


# Step 2: Get accent values for a specific language
def get_accent_values(lang_code):
    url = f"https://datasets-server.huggingface.co/rows?dataset=mozilla-foundation%2Fcommon_voice_17_0&config={lang_code}&split=train&offset=0&length=100"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 429:
            print(f"Rate limited on {lang_code}, sleeping 10s...")
            time.sleep(10)
            resp = requests.get(url, headers=HEADERS)
        if not resp.ok:
            print(f"Failed for {lang_code}: {resp.status_code}")
            return None
        rows = resp.json().get("rows", [])
        accents = set()
        for row in rows:
            accent = row.get("row", {}).get("accent")
            if accent:
                accents.add(accent)
        return len(accents)
    except Exception as e:
        print(f"Error for {lang_code}: {e}")
        return None


# Step 3: Process and save to CSV
def main():
    language_codes = get_language_codes()
    results = []
    success_count = 0
    fail_count = 0

    for idx, lang in enumerate(language_codes):
        print(f"[{idx+1}/{len(language_codes)}] Processing: {lang}")
        accent_count = get_accent_values(lang)
        results.append({"language_code": lang, "accent_count": accent_count})

        if accent_count is not None:
            success_count += 1
        else:
            fail_count += 1

        time.sleep(1.5)  # Add delay between requests

    # Save to CSV
    with open("language_accent_counts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["language_code", "accent_count"])
        writer.writeheader()
        writer.writerows(results)

    print("\nDone!")
    print(f"Successfully processed: {success_count}")
    print(f"Failed or no data:       {fail_count}")
    print("Saved results to language_accent_counts.csv")


if __name__ == "__main__":
    main()
