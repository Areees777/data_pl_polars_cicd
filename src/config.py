from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class Paths(BaseModel):
    base: str
    bronze: str
    silver: str
    gold: str


class Dataset(BaseModel):
    name: str
    input_path: str


class Features(BaseModel):
    enable_new_metric: bool = False
    drop_negative_amounts: bool = True


class RunCfg(BaseModel):
    write_format: Literal["parquet", "csv"] = "parquet"
    max_rows_smoke: int = 200


class AppConfig(BaseModel):
    env: Literal["dev", "staging", "prod"]
    paths: Paths
    dataset: Dataset
    features: Features = Field(default_factory=Features)
    run: RunCfg = Field(default_factory=RunCfg)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "AppConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)
