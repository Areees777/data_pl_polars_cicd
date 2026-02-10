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

Transforms a Polars LazyFrame of sales data by optionally filtering negative amounts, converting the amount column to float, and categorizing amounts into buckets.

Parameters:
lf: Polars LazyFrame containing sales data.
drop_negative_amounts: If True, removes rows with negative amounts.
enable_new_metric: If True, adds a new column amount_bucket with categories:
    <20 → "low"
    <50 → "mid"
    <100 → "high"
    >=100 → "vip"

Returns:
A transformed LazyFrame with the new numeric and optional categorical columns.

Behavior:
Filters out negative amounts if requested.
Converts amount to a float column amount_eur.
Adds amount_bucket categorization if enabled.
Maintains lazy evaluation until .collect() is called.

2. Writing Run Metadata

```
def write_run_metadata(
    *,
    output_root: str,
    env: str,
    input_path: str,
    output_version: str,
    git_sha: str | None,
    features: dict[str, Any],
    row_counts: dict[str, int],
) -> None:
    meta = {
        "env": env,
        "input": {"path": input_path},
        "output": {"dataset_root": output_root, "version": output_version},
        "git_sha": git_sha,
        "features": features,
        "row_counts": row_counts,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    path = Path(output_root) / f"run_{output_version}.json"
    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
```

Writes a JSON file containing metadata about a pipeline run, including environment, input/output info, git commit, features, row counts, and timestamp.

Parameters:
output_root: Directory where the metadata JSON will be saved.
env: Environment name (e.g., "dev" or "prod").
input_path: Path to the input data used in the run.
output_version: Version of the output dataset (used to name the metadata file).
git_sha: Git commit SHA of the current version, or None.
features: Dictionary describing which features were enabled during the run.
row_counts: Dictionary with row counts per table or dataset.

Returns:
None (creates a JSON file in output_root).

Behavior:
Builds a dictionary meta with all provided parameters plus a UTC timestamp created_at_utc.
Generates the output path as run_{output_version}.json inside output_root.
Writes the metadata dictionary to this JSON file with pretty formatting (2-space indentation).

3. CI/CD

The project uses GitHub Actions for automated checks:

Job build-and-deploy-dev:
Installs dependencies using Poetry
Runs linting (flake8)
Executes all unit tests (pytest)

The main branch is protected (Using rulesets in GitHub):
Only PRs from dev can be merged
Approval is required before merging
This ensures only validated code reaches the main branch.

## Usage

- Add more edge case unit tests to increase coverage
- Add visual documentation of the pipeline flow
- Structured logging for monitoring pipeline execution
- Prepare pipeline for automated deployment to different environments