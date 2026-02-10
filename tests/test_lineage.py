import json
from datetime import datetime
from src.lineage import write_run_metadata


def test_write_run_metadata(tmp_path):
    # Preparar datos de prueba
    output_root = tmp_path / "output"
    output_root.mkdir()
    env = "dev"
    input_path = "/fake/input/path"
    output_version = "v1"
    git_sha = "123abc"
    features = {"feature1": True, "feature2": False}
    row_counts = {"table1": 10, "table2": 5}

    # Llamar a la función
    write_run_metadata(
        output_root=str(output_root),
        env=env,
        input_path=input_path,
        output_version=output_version,
        git_sha=git_sha,
        features=features,
        row_counts=row_counts,
    )

    file_path = output_root / f"run_{output_version}.json"
    assert file_path.exists()

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["env"] == env
    assert data["input"]["path"] == input_path
    assert data["output"]["dataset_root"] == str(output_root)
    assert data["output"]["version"] == output_version
    assert data["git_sha"] == git_sha
    assert data["features"] == features
    assert data["row_counts"] == row_counts
    datetime.fromisoformat(data["created_at_utc"].replace("Z", "+00:00"))
