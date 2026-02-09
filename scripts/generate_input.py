import os
from datetime import datetime, timedelta

import numpy as np
import polars as pl


def main():
    os.makedirs("./data/dev/input", exist_ok=True)
    rng = np.random.default_rng(42)

    n = 2000
    start = datetime(2026, 1, 1, 0, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(n)]

    df = pl.DataFrame(
        {
            "date": dates,
            "customer_id": rng.integers(1, 200, size=n),
            "amount": np.round(rng.normal(50, 30, size=n), 2),
            "country": rng.choice(["ES", "FR", "DE", "IT"], size=n),
        }
    )

    # algunos negativos para probar gate
    idx = rng.choice(n, size=50, replace=False)
    df = df.with_columns(
        pl.when(pl.int_range(0, n).is_in(idx))
        .then(pl.col("amount") * -1)
        .otherwise(pl.col("amount"))
        .alias("amount")
    )

    df.write_csv("./data/dev/input/sales.csv")
    print("✅ Generated ./data/dev/input/sales.csv")


if __name__ == "__main__":
    main()
