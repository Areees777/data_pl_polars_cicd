from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

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

