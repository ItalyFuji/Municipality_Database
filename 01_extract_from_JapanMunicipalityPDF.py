import re
import pdfplumber
import pandas as pd
from pathlib import Path
import jaconv # from full-width katakana to hiragana

PDF_PATH = Path("data_raw/Japan_Municipality.pdf")
OUTPUT_PATH = Path("data_output/01_raw_masterDB.csv")

CODE_PATTERN = re.compile(r"^[0-9]{6}$")

def main():
    records = []

    # PDF to table
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:

            table = page.extract_table()

            if not table:
                continue


            for row in table:

                # Structural check: Skip rows with insufficient columns to prevent index errors
                if row is None or len(row) < 5:
                    continue

                try:
                    code = row[0]           # 団体コード / Municipality_Code
                    prefecture = row[1]     # 都道府県名(漢字) / Prefecture_Name(kanji)
                    municipality = row[2]   # 市区町村名(漢字) / Municipality_Name(Kanji)
                    reading_kana = row[4]   # 市区町村名(カタカナ) / Municipality_Name(katakana)

                    # Header noise check: Skip rows where the table header (e.g. "団体コード")
                    # was captured as a data row (happens once at the top of each sub-table)
                    if not code or not CODE_PATTERN.match(str(code).strip()):
                        continue

                    # Content check: Skip rows with empty municipality names (e.g., prefecture-only rows)
                    if code and municipality and str(municipality).strip() != "":
                        municipality = municipality.replace('\n', '')
                        reading_kana = reading_kana.replace('\n', '') if reading_kana else ""

                        # Normalize reading: Convert half-width katakana to hiragana
                        reading_kana = jaconv.kata2hira(jaconv.hankaku2zenkaku(reading_kana))

                        records.append([
                            code,
                            prefecture,
                            municipality,
                            reading_kana
                        ])
                except IndexError:
                    continue

    # table to Database
    df = pd.DataFrame(
        records,

        columns=[
            "municipality_code",
            "prefecture",
            "municipality_name",
            "reading_hiragana"
        ]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print("Extracted Municipality")

if __name__ == "__main__":
    main()
