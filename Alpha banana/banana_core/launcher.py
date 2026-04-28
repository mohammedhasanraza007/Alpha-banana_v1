import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

USE_STREAMLIT = True

# 🟢 SAFE ADDITION: model preload hook
def ensure_model_ready():
    try:
        from AlphaBananaCore.model_loader import ensure_model
        ensure_model()
    except Exception as e:
        print("[Alpha Banana] Model check failed:", e)
        print("[Alpha Banana] Continuing anyway...")

def main():
    print("=" * 60)
    print(" Alpha Banana v1 - Local Image Generator")
    print("=" * 60)

    # 🟢 SAFE INJECTION POINT (BEFORE UI START)
    print("[Alpha Banana] Checking AI model...")
    ensure_model_ready()

    if USE_STREAMLIT:
        app_path = PROJECT_ROOT / "streamlit_app.py"
        print(f"[Alpha Banana] Launching Streamlit UI: {app_path}")
        os.system(f"streamlit run \"{app_path}\"")
    else:
        from banana_ui.ui import build_ui
        print("[Alpha Banana] Launching Gradio UI")
        demo = build_ui()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
        )

if __name__ == "__main__":
    main()