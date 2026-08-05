import pandas as pd

# これらはassertで正誤を判定する単体テストではなく、
# 各ステップの中間データを可視化するためのレポート。
# `pytest test_reports.py -s -v` のように -s を付けないと出力が表示されない。

CATEGORY_ORDER = ["市", "町", "村", "区"]

def classify_by_suffix(name):
    for suffix in CATEGORY_ORDER:
        if str(name).endswith(suffix):
            return suffix
    return None


def test_category_distribution_after_02():
    df = pd.read_csv("data_output/02_dedup_masterDB.csv", dtype=str)
    df["category"] = df["municipality_name"].apply(classify_by_suffix)
    total = len(df)

    print("\n=== 02完了後（完全重複行削除後）の種別分布 ===")
    counts = df["category"].value_counts().reindex(CATEGORY_ORDER, fill_value=0)
    for category, count in counts.items():
        print(f"{category}: {count}件 ({count / total:.1%})")

    print("\n=== 都道府県別の内訳 ===")
    crosstab = pd.crosstab(df["prefecture"], df["category"])
    crosstab = crosstab.reindex(columns=CATEGORY_ORDER, fill_value=0)
    print(crosstab.to_string())


def test_duplicate_municipality_names_after_04():
    df = pd.read_csv("data_output/04_normalized_masterDB.csv", dtype=str)

    dup = df[df.duplicated(subset=["municipality_name"], keep=False)]

    print("\n=== 04完了後、市区町村名（漢字）が重複する組み合わせ ===")
    for name, group in dup.groupby("municipality_name", sort=False):
        members = ", ".join(
            f"{row.municipality_code}({row.prefecture})" for row in group.itertuples()
        )
        print(f"{name}: {members}")


def test_kanji_name_length_distribution_final():
    df = pd.read_csv("data_output/municipality_DB.csv", dtype=str)
    total = len(df)

    print("\n=== 完成版：漢字表記(name_short、種別除く)の文字数分布 ===")
    counts = df["name_short"].str.len().value_counts().sort_index()
    for length, count in counts.items():
        print(f"{length}文字: {count}件 ({count / total:.1%})")


def test_reading_length_distribution_final():
    df = pd.read_csv("data_output/municipality_DB.csv", dtype=str)
    total = len(df)

    print("\n=== 完成版：ひらがな表記(reading_short、種別除く)の文字数分布 ===")
    counts = df["reading_short"].str.len().value_counts().sort_index()
    for length, count in counts.items():
        print(f"{length}文字: {count}件 ({count / total:.1%})")
