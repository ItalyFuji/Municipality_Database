# Municipality_Database

総務省が発行する全国地方公共団体コードから、日本全国の市区町村の名称・読み仮名・種別を抽出・整形するツールです。

A tool that extracts and normalizes municipality names, readings, and categories from the Japanese Municipality Code PDF published by the Ministry of Internal Affairs and Communications.

---

## Overview / 概要

PDFから市区町村データを抽出し、5段階のステップを経て正規化されたCSVデータベースを生成します。

Extracts municipality data from a PDF and generates a normalized CSV database through 5 sequential steps.

```
data_raw/Japan_Municipality.pdf
        │
        ▼
01_extract_from_JapanMunicipalityPDF.py   PDF抽出 + ヘッダー混入行の除去
        │                                  Extract from PDF + remove header noise rows
        ▼
data_output/01_raw_masterDB.csv
        │
        ▼
02_remove_exact_duplicates.py             完全重複行の削除（政令市が区一覧の直前に再掲される分など）
        │                                  Remove fully identical duplicate rows
        ▼
data_output/02_dedup_masterDB.csv
        │
        ▼
03_remove_wards.py                        政令指定都市の区を除外（東京都特別区23区は残す）
        │                                  Remove designated-city wards (Tokyo's 23 special wards are kept)
        ▼
data_output/03_no_ward_masterDB.csv
        │
        ▼
04_normalize_municipality.py              種別判定（市・町・村・区）と短縮名・短縮読みの生成
        │                                  Classify category and generate short name/reading
        ▼
data_output/04_normalized_masterDB.csv
        │
        ▼
05_remove_name_duplicates.py              同一都道府県内で名称・読みが完全一致する行の削除
        │                                  Remove same-prefecture name+reading duplicates
        ▼
data_output/municipality_DB.csv
```

---

## Requirements / 必要なパッケージ

```bash
pip install -r requirements.txt
```

| Package | Purpose（用途） |
|---|---|
| pdfplumber | PDFからテーブルを抽出 / Extract tables from PDF |
| pandas | データ整形・CSV出力 / Data processing and CSV output |
| jaconv | カタカナ→ひらがな変換 / Convert katakana to hiragana |
| pytest | テスト実行 / Run tests |

---

## Setup / 準備

総務省のページから全国地方公共団体コードのPDFをダウンロードし、`data_raw/` フォルダに `Japan_Municipality.pdf` という名前で保存してください。

Download the municipality code PDF from the Ministry of Internal Affairs and Communications website and place it in the `data_raw/` folder as `Japan_Municipality.pdf`.

- ページ / Page: https://www.soumu.go.jp/denshijiti/code.html
- PDF直リンク / Direct PDF link: https://www.soumu.go.jp/main_content/000925834.pdf

> **注意 / Note:** PDF直リンクのURLは総務省の更新に伴い変更される場合があります。リンク切れの場合は上記ページから最新版をダウンロードしてください。
> The direct PDF link may change when the Ministry updates the file. If the link is broken, download the latest version from the page above.

```
Municipality_Database/
├── data_raw/
│   └── Japan_Municipality.pdf   ← ここに置く / Place the PDF here
└── data_output/                 ← 出力先 / Output folder
```

## Usage / 使い方

### Option A: Run all steps at once / まとめて実行

```bat
run.bat
```

### Option B: Run step by step / ステップごとに実行

#### Step 1: Extract data from PDF / PDFからデータ抽出

```bash
python 01_extract_from_JapanMunicipalityPDF.py
```

`data_raw/Japan_Municipality.pdf` を読み込み、団体コードが6桁の数字でない行（PDFのページヘッダーが誤って抽出された行）を除いた `data_output/01_raw_masterDB.csv` を生成します。

Reads `data_raw/Japan_Municipality.pdf`, drops rows whose code isn't a 6-digit number (page headers mistakenly captured as data rows), and generates `data_output/01_raw_masterDB.csv`.

#### Step 2: Remove exact duplicate rows / 完全重複行の削除

```bash
python 02_remove_exact_duplicates.py
```

全カラムが完全に一致する行を削除します（政令指定都市が区の一覧の直前に再掲されるケースなど）。`data_output/02_dedup_masterDB.csv` を生成します。

Removes rows that are fully identical across all columns (e.g. a designated city restated right before its ward listing). Generates `data_output/02_dedup_masterDB.csv`.

#### Step 3: Remove wards / 区の除外

```bash
python 03_remove_wards.py
```

政令指定都市の行政区（例：札幌市中央区）を除外します。政令指定都市の区は独立した地方公共団体ではなく市の内部組織であるため対象ですが、東京都特別区（例：千代田区）は地方自治法上「市に準ずる基礎的地方公共団体」であり、市町村と同格の主体として残します。`data_output/03_no_ward_masterDB.csv` を生成します。

Removes designated-city administrative wards (e.g. 札幌市中央区), which are internal subdivisions of a city rather than independent local governments. Tokyo's 23 special wards (e.g. 千代田区) are kept, since under the Local Autonomy Act they are treated as basic local governments on par with municipalities. Generates `data_output/03_no_ward_masterDB.csv`.

#### Step 4: Normalize categories and short names / 種別判定・短縮名生成

```bash
python 04_normalize_municipality.py
```

市区町村名の末尾（市・町・村・区）から種別を判定し、種別を除いた短縮名・短縮読みを生成します。`data_output/04_normalized_masterDB.csv` を生成します。

Classifies each row's category (市/町/村/区) from its name suffix and generates a short name/reading with the suffix removed. Generates `data_output/04_normalized_masterDB.csv`.

#### Step 5: Remove same-prefecture name duplicates / 同一都道府県内の名称重複削除

```bash
python 05_remove_name_duplicates.py
```

同一都道府県内で都道府県名・市区町村名（漢字）・読み仮名が全て一致する行を、最初に出現したものだけ残して削除します（例：北海道に2つ存在する「泊村」）。削除された組み合わせはコンソールに表示されます。`data_output/municipality_DB.csv` を生成します。

Within the same prefecture, if prefecture + kanji name + reading are all identical, keeps only the first occurrence and drops the rest (e.g. Hokkaido has two 泊村 with different codes). Prints which rows were merged. Generates `data_output/municipality_DB.csv`.

> 都道府県をまたいだ同名の市区町村（例：伊達市は北海道と福島県の両方に存在）は削除されません。名前だけで一意に識別できない場合は、都道府県とセットで扱ってください。
> Same-named municipalities across different prefectures (e.g. 伊達市 exists in both Hokkaido and Fukushima) are not removed. When a name alone isn't unique, pair it with its prefecture.

---

## Output Format / 出力フォーマット

`municipality_DB.csv` のカラム構成 / Column structure of `municipality_DB.csv`:

| Column | Description | Example |
|---|---|---|
| `municipality_code` | 団体コード / Municipality code | `011002` |
| `prefecture` | 都道府県名 / Prefecture name | `北海道` |
| `municipality_name` | 市区町村名（正式名称）/ Full municipality name | `札幌市` |
| `reading_hiragana` | 読み仮名（ひらがな）/ Reading in hiragana | `さっぽろし` |
| `municipality_category` | 種別（市・町・村・区）/ Category | `市` |
| `name_short` | 短縮名（種別suffix除去）/ Short name | `札幌` |
| `reading_short` | 短縮読み（suffix除去）/ Short reading | `さっぽろ` |

---

## Testing / テスト

```bash
pytest -v
```

| File | 内容 / Content |
|---|---|
| `test_normalize.py` | `04_normalize_municipality.py` の `format_municipality()` の単体テスト / Unit tests for `format_municipality()` |
| `test_remove_wards.py` | `03_remove_wards.py` の `is_ward()` の単体テスト（政令市の区と東京特別区の判別を含む）/ Unit tests for `is_ward()`, including designated-city ward vs. Tokyo special ward |
| `test_reports.py` | 正誤判定用のテストではなく、各ステップ完了後のデータを集計・表示するレポート。`pytest test_reports.py -s -v` のように `-s` を付けないと出力が表示されない / Not correctness tests — these print aggregate statistics after each step. Requires `-s` to see the output |

---

## Notes / 注意事項

- 政令指定都市の行政区（例：札幌市中央区）は除外されますが、東京都特別区23区（例：千代田区）は市町村と同格の地方公共団体として残されます / Designated-city wards (e.g. 札幌市中央区) are excluded, but Tokyo's 23 special wards (e.g. 千代田区) are kept as municipality-equivalent local governments.
- 読み仮名は半角・全角カタカナをひらがなに正規化します / Readings are normalized from katakana (half/full-width) to hiragana.
- 都道府県をまたいだ同名の市区町村は残ります。名前だけでは一意に識別できないため、利用時は都道府県とセットで扱ってください / Same-named municipalities across different prefectures are kept; pair a name with its prefecture when uniqueness matters.
- 出力CSVのエンコーディングは `UTF-8 BOM付き` です（Excel対応）/ Output CSV is encoded in `UTF-8 with BOM` for Excel compatibility.
