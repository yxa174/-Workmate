import pytest
from csv_processor import filter_data, aggregate_data, read_csv
from typing import List, Dict
from typing import List, Dict, Union


@pytest.fixture
def sample_data() -> List[Dict[str, Union[str, float]]]:
    return [
        {"name": "iphone", "brand": "apple", "price": "999", "rating": "4.9"},
        {"name": "galaxy", "brand": "samsung", "price": "1199", "rating": "4.8"},
        {"name": "redmi", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    ]


def test_filter_data_eq(sample_data):
    filtered = filter_data(sample_data, "brand", "==", "apple")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "iphone"


def test_filter_data_gt(sample_data):
    filtered = filter_data(sample_data, "price", ">", "500")
    assert len(filtered) == 2


def test_aggregate_avg(sample_data):
    assert aggregate_data(sample_data, "price", "avg") == pytest.approx(798.33, 0.01)


def test_aggregate_min(sample_data):
    assert aggregate_data(sample_data, "rating", "min") == 4.6


def test_read_csv(tmp_path):
    csv_content = """name,brand,price,rating
iphone,apple,999,4.9"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    data = read_csv(str(file_path))
    assert len(data) == 1
    assert data[0]["brand"] == "apple"
