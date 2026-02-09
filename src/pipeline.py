import argparse
import os

import polars as pl

from config import AppConfig
from lineage import write_run_metadata
from steps.extract import extract_csv
from steps.load import load_versioned
from steps.transform import transform_sales


def get_env() -> str:
    # default a dev si no está definida
    return os.getenv("APP_ENV", "dev")


def load_config(path: str) -> AppConfig:
    cfg = AppConfig.from_yaml(path)
    return cfg


def run_pipeline(cfg: AppConfig, *, smoke: bool = False) -> dict:
    git_sha = os.getenv("GIT_SHA")
    lf = extract_csv(cfg.dataset.input_path)

    in_rows = lf.select(pl.len()).collect().item()

    if smoke:
        lf = lf.limit(cfg.run.max_rows_smoke)

    lf_t = transform_sales(
        lf,
        drop_negative_amounts=cfg.features.drop_negative_amounts,
        enable_new_metric=cfg.features.enable_new_metric,
    )

    df_out = lf_t.collect()
    out_rows = df_out.height

    dataset_root = f"{cfg.paths.silver}/{cfg.dataset.name}"
    info = load_versioned(
        df_out,
        dataset_root=dataset_root,
        write_format=cfg.run.write_format,
        git_sha=git_sha,
    )

    write_run_metadata(
        output_root=dataset_root,
        env=cfg.env,
        input_path=cfg.dataset.input_path,
        output_version=info.version_id,
        git_sha=git_sha,
        features=cfg.features.model_dump(),
        row_counts={"input": in_rows, "output": out_rows},
    )


def main():
    env = get_env()

    parser = argparse.ArgumentParser(description="Run data pipeline")
    parser.add_argument(
        "--smoke",
        action="store_true",  # es un flag, True si está presente
        help="Ejecutar en modo smoke (prueba rápida con pocas filas)",
    )
    args = parser.parse_args()

    cfg = load_config(f"config/{env}.yaml")
    run_pipeline(cfg, smoke=args.smoke)


if __name__ == "__main__":
    main()
