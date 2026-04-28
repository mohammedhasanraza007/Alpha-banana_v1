from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from banana_core.hardware_detect import get_device
from huggingface_hub import hf_hub_download

# =========================
# PATHS
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = PROJECT_ROOT / "models" / "checkpoints"

# ONLY ONE FILE — NO PIPELINE
MODEL_FILE = "v1-5-pruned-emaonly.safetensors"

# =========================
# FORCE SINGLE FILE DOWNLOAD ONLY
# =========================
def ensure_model():

    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = CHECKPOINTS_DIR / MODEL_FILE

    # If already exists → DO NOTHING
    if model_path.exists():
        print("[Alpha Banana] Using existing EMA-only model.")
        return str(model_path)

    print("[Alpha Banana] Downloading ONLY 4GB EMA-only model...")

    downloaded_path = hf_hub_download(
        repo_id="runwayml/stable-diffusion-v1-5",
        filename=MODEL_FILE,
        local_dir=str(CHECKPOINTS_DIR),
        local_dir_use_symlinks=False
    )

    print("[Alpha Banana] Model ready:", downloaded_path)
    return downloaded_path


# =========================
# LIST MODELS (ONLY ONE ALLOWED)
# =========================
def list_models():

    ensure_model()

    return [MODEL_FILE] if (CHECKPOINTS_DIR / MODEL_FILE).exists() else []


# =========================
# LOAD MODEL (SINGLE FILE ONLY)
# =========================
def load_model(filename):

    ensure_model()

    path = CHECKPOINTS_DIR / MODEL_FILE

    if not path.exists():
        raise FileNotFoundError(path)

    device = get_device()
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_single_file(
        str(path),
        torch_dtype=dtype,
        safety_checker=None
    )

    pipe = pipe.to(device)

    if device == "cpu":
        pipe.enable_attention_slicing()

    return pipe