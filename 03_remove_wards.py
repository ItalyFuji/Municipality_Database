import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data_output/02_dedup_masterDB.csv")
OUTPUT_PATH = Path("data_output/03_no_ward_masterDB.csv")

def is_ward(name):
    # Designated-city administrative wards only (e.g. 札幌市中央区).
    # Tokyo's 23 special wards (e.g. 千代田区) are independent local governments
    # and don't contain "市" in their name, so they are kept.
    name = str(name)
    return name.endswith("区") and "市" in name

def main():
    df = pd.read_csv(INPUT_PATH, dtype=str)

    # Remove designated-city wards; Tokyo's 23 special wards are kept
    df = df[~df["municipality_name"].apply(is_ward)]

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Removed ward rows")

if __name__ == "__main__":
    main()
