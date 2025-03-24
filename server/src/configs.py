from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODEL_DIR = PROJ_ROOT / "models"

LOG_DIR = PROJ_ROOT / "logs"

CRF_CONFIG = {
     "algorithm": "lbfgs",
     "c1": 0.1,
     "c2": 0.1,
     "max_iterations": 100,
     "all_possible_transitions": True,
     "verbose": True,
     "model_path": f"{MODEL_DIR}/crf_model.pkl" 
}

LEN_TRAIN_DATA = 2000
LEN_DEV_DATA = 400

if __name__ == "__main__":
     print(f"PROJ_ROOT path is: {PROJ_ROOT}")
     print(f"DATA_DIR path is: {DATA_DIR}")
     print(f"RAW_DATA_DIR path is: {RAW_DATA_DIR}")
     print(f"PROCESSED_DATA_DIR path is: {PROCESSED_DATA_DIR}")
     print(f"MODEL_DIR path is: {MODEL_DIR}")