# Data Pipeline CI/CD with Polars

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![CI](https://github.com/Areees777/data_polars_cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/Areees777/data_polars_cicd/actions/workflows/ci.yml)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

## Description

This project is a **data pipeline** built with **Polars** and Python 3.11, fully managed with **CI/CD** using **GitHub Actions**.  
It allows transforming data, generating metrics, and keeping a **run metadata record** in a reproducible and testable way.

The project follows professional data engineering practices:  
- Code linting and formatting with **flake8 + black**  
- Dependency management and virtual environments with **Poetry**  
- Pre-commit hooks to enforce code quality  
- Unit tests for all functions  
- CI/CD for automated quality checks and safe deployments

---

## Project Structure
data_polars_cicd/
├─ src/
│ ├─ steps/
| ├─├─ extract.py # Data extraction functions
│ │ ├─ transform.py # Data transformation functions
│ │ └─ load.py # Data load functions
│ └─ config.py # Config functions to load the configurations based on the environment 
│ └─ lineage.py # Lineage functions to write metadata
│ └─ pipeline.py # Main script to run the all pipeline step by step
├─ tests/
│ ├─ test_transform.py # Unit tests for transform_sales
│ └─ test_lineage.py # Unit tests for write_run_metadata
├─ pyproject.toml
├─ poetry.lock
├─ README.md
└─ .github/workflows/ci.yml # yaml to define DEV github action
└─ .github/workflows/release.yml # yaml to define PROD github action

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Areees777/data_polars_cicd.git
cd data_polars_cicd

curl -sSL https://install.python-poetry.org | python3 -

poetry install

```

## Usage

1. Data Transformation
```
from src.steps.transform import transform_sales
import polars as pl

lf = pl.DataFrame({
    "amount": [10, -5, 0],
    "date": ["2026-01-01"]*3,
    "customer_id": [1,2,3],
    "country": ["ES"]*3
}).lazy()

out = transform_sales(lf, drop_negative_amounts=True, enable_new_metric=False).collect()
```