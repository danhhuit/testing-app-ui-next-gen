import os
import subprocess
from pathlib import Path


def test_k6_saucedemo_smoke():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / "performance" / "saucedemo_smoke.js"

    k6_bin = os.environ.get("K6_BIN", r"C:\Program Files\k6\k6.exe")

    result = subprocess.run(
        [k6_bin, "run", str(script_path)],
        capture_output=True,
        text=True,
        timeout=180,
    )

    output = result.stdout + "\n" + result.stderr
    assert result.returncode == 0, output
