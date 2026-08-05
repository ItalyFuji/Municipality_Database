import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data_output/03_no_ward_masterDB.csv")
OUTPUT_PATH = Path("data_output/04_normalized_masterDB.csv")

def format_municipality(row):
    kanji = str(row["municipality_name"])
    gana = str(row["reading_hiragana"])

    category = None
    short_kanji = kanji
    short_gana = gana

    # Handle Cities (市)
    if kanji.endswith("市"):
        short_kanji = kanji[:-1]
        category = "市"
        if gana.endswith("し"):
            short_gana = gana[:-1]

    # Handle Towns (町)
    elif kanji.endswith("町"):
        short_kanji = kanji[:-1]
        category = "町"
        if gana.endswith("まち"):
            short_gana = gana[:-2]
        elif gana.endswith("ちょう"):
            short_gana = gana[:-3]

    # Handle Villages (村)
    elif kanji.endswith("村"):
        short_kanji = kanji[:-1]
        category = "村"
        if gana.endswith("むら"):
            short_gana = gana[:-2]
        elif gana.endswith("そん"):
            short_gana = gana[:-2]

    # Handle Tokyo's 23 special wards (区)
    elif kanji.endswith("区"):
        short_kanji = kanji[:-1]
        category = "区"
        if gana.endswith("く"):
            short_gana = gana[:-1]

    return pd.Series([category, short_kanji, short_gana])

def main():
    df = pd.read_csv(INPUT_PATH, dtype=str)

    df[["municipality_category", "name_short", "reading_short"]] = df.apply(format_municipality, axis=1)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print("Normalized municipality categories and short names")

if __name__ == "__main__":
    main()
