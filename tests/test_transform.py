import polars as pl
from src.steps.transform import transform_sales

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))


def test_drop_negative_amounts():
    lf = pl.DataFrame(
        {
            "amount": [10, -5, 0],
            "date": ["2026-01-01"] * 3,
            "customer_id": [1, 2, 3],
            "country": ["ES"] * 3,
        }
    ).lazy()

    out = transform_sales(
        lf, drop_negative_amounts=True, enable_new_metric=False
    ).collect()
    assert out.filter(pl.col("amount") < 0).height == 0
