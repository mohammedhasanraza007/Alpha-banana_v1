import torch


def get_device():

    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        print(f"[Alpha Banana] NVIDIA GPU detected: {name}")
        return "cuda"

    print("[Alpha Banana] No CUDA GPU detected. Using CPU.")
    return "cpu"