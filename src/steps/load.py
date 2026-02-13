from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import polars as pl


@dataclass
class VersionInfo:
    version_id: str
    path: Path
    git_sha: str | None
    timestamp: datetime


def ensure_dir(path: str | Path):
    # En caso de que la carpeta no exista donde se almacenan los versionados entonces la crea
    Path(path).mkdir(parents=True, exist_ok=True)


def new_version_id() -> str:
    """Genera un ID de versión basado en timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_latest_pointer(latest_path: Path, version_path: Path):
    """Crea un puntero al último dataset guardado."""
    latest_path.write_text(str(version_path))


def load_versioned(
    df: pl.DataFrame | pl.LazyFrame,
    *,
    dataset_root: str,
    write_format: str = "parquet",
    git_sha: str | None = None,
) -> VersionInfo:
    """
    Guarda un DataFrame o LazyFrame versionado en parquet.

    Args:
        df: DataFrame o LazyFrame de Polars
        dataset_root: directorio base donde guardar versiones
        write_format: "parquet" o "csv" (recomendado parquet)
        git_sha: SHA opcional de git para trazabilidad

    Returns:
        VersionInfo con metadata de la versión guardada
    """

    ensure_dir(dataset_root)

    version_id = new_version_id()
    version_path = Path(dataset_root) / version_id
    ensure_dir(version_path)

    filename = f"data.{write_format}"
    file_path = version_path / filename

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    if write_format == "parquet":
        df.write_parquet(file_path)
    else:
        raise ValueError(f"Unsupported write_format: {write_format}")

    # Escribimos el path del ultimo parquet para leer solo los datos del LATEST
    latest_pointer = Path(dataset_root) / "LATEST"
    write_latest_pointer(latest_pointer, file_path)

    return VersionInfo(
        version_id=version_id, path=file_path, git_sha=git_sha, timestamp=datetime.now()
    )
