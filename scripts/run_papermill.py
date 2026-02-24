"""
Run all notebooks in pipeline using Papermill
Reproducible execution script
"""

import papermill as pm
from pathlib import Path
import yaml
import logging
from datetime import datetime

# =============================
# Setup logging
# =============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# =============================
# Paths
# =============================
ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"
OUTPUT_DIR = ROOT / "outputs" / "notebooks"
CONFIG_PATH = ROOT / "configs" / "params.yaml"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================
# Load parameters
# =============================
def load_params():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}

params = load_params()

# =============================
# Notebook execution order
# =============================
PIPELINE = [
    "01_eda.ipynb",
    "02_preprocess_feature.ipynb",
    "03_mining_or_clustering.ipynb",
    "04_modeling.ipynb",
    "04b_semi_supervised.ipynb",
    "05_evaluation_report.ipynb"
]

# =============================
# Runner
# =============================
def run_notebook(nb_name):
    input_path = NOTEBOOK_DIR / nb_name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"{nb_name.replace('.ipynb','')}_{timestamp}.ipynb"

    logger.info(f"Running {nb_name}")

    pm.execute_notebook(
        input_path=str(input_path),
        output_path=str(output_path),
        parameters=params,
        log_output=True,
        kernel_name="python3" 
    )

    logger.info(f"Finished {nb_name}")
    return output_path


# =============================
# Main pipeline
# =============================
def main():

    logger.info("START PIPELINE EXECUTION")

    for nb in PIPELINE:
        try:
            run_notebook(nb)
        except Exception as e:
            logger.error(f"FAILED at {nb}")
            raise e

    logger.info("PIPELINE FINISHED SUCCESSFULLY")


if __name__ == "__main__":
    main()