import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data_output/01_raw_masterDB.csv")
OUTPUT_PATH = Path("data_output/02_dedup_masterDB.csv")

def main():
    df = pd.read_csv(INPUT_PATH, dtype=str)

    # Remove fully identical rows (e.g. designated cities restated
    # right before their ward listing, with the same code/prefecture/name/reading)
    df = df.drop_duplicates(keep="first")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Removed exact duplicate rows")

if __name__ == "__main__":
    main()
