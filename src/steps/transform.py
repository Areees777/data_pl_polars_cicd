import polars as pl

def transform_sales(
    lf: pl.LazyFrame,
    *,
    drop_negative_amounts: bool,
    enable_new_metric: bool
) -> pl.LazyFrame:
    
    if drop_negative_amounts:
        lf = lf.filter(pl.col("amount") >= 0)

    lf = lf.with_columns(
        pl.col("amount").cast(pl.Float64).alias("amount_eur")
    )

    if enable_new_metric:
        lf = lf.with_columns(
            pl.when(pl.col("amount_eur") < 20).then(pl.lit("low"))
            .when(pl.col("amount_eur") < 50).then(pl.lit("mid"))
            .when(pl.col("amount_eur") < 100).then(pl.lit("high"))
            .otherwise(pl.lit("vip"))
            .alias("amount_bucket")
        )
    
    return lf


