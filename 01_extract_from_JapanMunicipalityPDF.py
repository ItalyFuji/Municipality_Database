import pdfplumber
import pandas as pd
from pathlib import Path

PDF_PATH = Path("data_raw/Japan_Municipality.pdf")
OUTPUT_PATH = Path("data_output/raw_masterDB.csv")

def main():
    records = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if not table:
                continue
            
            for row in table[1:]:
                if row is None or len(row) < 5:
                    continue
                try:
                    code = row[0]
                    prefecture = row[1]
                    municipality = row[2]
                    reading_kana = row[4]

                    if code and municipality and str(municipality).strip() != "":
                        municipality = municipality.replace('\n', '')
                        reading_kana = reading_kana.replace('\n', '') if reading_kana else ""
                        records.append([
                            code,
                            prefecture,
                            municipality,
                            reading_kana
                        ])
                except IndexError:
                   continue
    df = pd.DataFrame(
        records,
        columns=[
            "municipality_code",
            "prefecture",
            "municipality_name",
            "reading_katakana"
        ]
    )

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print("Extracted Municipality")

if __name__ == "__main__":
    main()
