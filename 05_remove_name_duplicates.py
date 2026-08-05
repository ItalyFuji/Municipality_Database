import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data_output/04_normalized_masterDB.csv")
OUTPUT_PATH = Path("data_output/municipality_DB.csv")

DEDUP_KEYS = ["prefecture", "municipality_name", "reading_hiragana"]

def main():
    df = pd.read_csv(INPUT_PATH, dtype=str)

    # Report which rows will be merged away before dropping them
    # (e.g. 北海道 has two 泊村 with different codes; keep the first occurrence)
    dup_mask = df.duplicated(subset=DEDUP_KEYS, keep=False)
    for _, group in df[dup_mask].groupby(DEDUP_KEYS, sort=False):
        kept, dropped_rows = group.iloc[0], group.iloc[1:]
        for _, dropped in dropped_rows.iterrows():
            print(
                f"統合: {dropped['municipality_code']} {dropped['prefecture']}{dropped['municipality_name']} "
                f"→ {kept['municipality_code']} {kept['prefecture']}{kept['municipality_name']} に統合"
            )

    df = df.drop_duplicates(subset=DEDUP_KEYS, keep="first")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print("Removed same-prefecture name duplicates")

if __name__ == "__main__":
    main()
