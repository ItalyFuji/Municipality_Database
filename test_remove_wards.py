import importlib.util
from pathlib import Path

# 03_remove_wards.py はファイル名が数字始まりのため importlib で読み込む
spec = importlib.util.spec_from_file_location(
    "remove_wards", Path(__file__).parent / "03_remove_wards.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

is_ward = module.is_ward


def test_ward_with_city_prefix_is_detected():
    assert is_ward("札幌市中央区") is True

def test_tokyo_special_ward_is_not_ward():
    # 「市」を含まないので政令市の区ではなく、独立した地方公共団体として残す
    assert is_ward("千代田区") is False

def test_tokyo_special_ward_same_name_as_a_designated_city_ward_is_not_ward():
    # 東京都中央区と札幌市中央区のような同名衝突でも、「市」の有無で正しく区別できる
    assert is_ward("中央区") is False

def test_city_is_not_ward():
    assert is_ward("札幌市") is False

def test_town_is_not_ward():
    assert is_ward("能勢町") is False

def test_village_is_not_ward():
    assert is_ward("檜原村") is False
