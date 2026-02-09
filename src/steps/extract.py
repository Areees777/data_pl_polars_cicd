import polars as pl


def extract_csv(path: str) -> pl.LazyFrame:
    # LazyFrame = bueno para “mentalidad DE”: pipeline declarativo
    return pl.scan_csv(path, try_parse_dates=True)
