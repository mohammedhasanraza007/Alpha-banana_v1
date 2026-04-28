"""
streamlit_ui.py
---------------
Streamlit UI for Alpha Banana v1.
"""

import datetime
from pathlib import Path

import streamlit as st
import torch

from banana_core.model_loader import list_models, load_model

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

APP_TITLE = "Alpha Banana v1"
APP_DESCRIPTION = "solo made by- Mohammed Hasan Raza."


def _get_pipe(name: str, low_vram: bool):
    """Cache pipeline in session_state so we don't reload on every click."""
    cache = st.session_state.setdefault(
        "_loaded", {"name": None, "pipe": None, "low_vram": None}
    )

    if (
        cache["pipe"] is None
        or cache["name"] != name
        or cache["low_vram"] != low_vram
    ):
        pipe = load_model(name)

        if low_vram:
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()

        cache["pipe"] = pipe
        cache["name"] = name
        cache["low_vram"] = low_vram

    return cache["pipe"]


def _unload_pipe():
    cache = st.session_state.get("_loaded")
    if cache is not None:
        cache["pipe"] = None
        cache["name"] = None
        cache["low_vram"] = None

    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def _generate_image(
    prompt: str,
    negative_prompt: str,
    model_name: str,
    steps: int,
    guidance: float,
    width: int,
    height: int,
    seed: int,
    low_vram: bool,
):
    pipe = _get_pipe(model_name, low_vram)

    generator = None
    if seed != -1:
        generator = torch.manual_seed(int(seed))

    result = pipe(
        prompt=str(prompt),
        negative_prompt=str(negative_prompt or ""),
        num_inference_steps=int(steps),
        guidance_scale=float(guidance),
        width=int(width),
        height=int(height),
        generator=generator,
    )
    image = result.images[0]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUTS_DIR / f"{timestamp}.png"
    image.save(out_path)

    return image, out_path


def render_ui():
    st.set_page_config(page_title=APP_TITLE, page_icon=":banana:", layout="wide")

    st.title(APP_TITLE)
    st.caption(APP_DESCRIPTION)

    models = list_models()

    with st.sidebar:
        st.header("Settings")

        if not models:
            st.warning(
                "No models found. Place a .safetensors file in "
                "models/checkpoints/ and refresh."
            )
            model_name = None
        else:
            model_name = st.selectbox("Model", options=models, index=0)

        if st.button("Refresh model list"):
            st.rerun()

        low_vram = st.checkbox("Low VRAM Mode", value=False)

        if st.button("Unload model"):
            _unload_pipe()
            st.success("Model unloaded.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        prompt = st.text_area(
            "Prompt",
            value="",
            height=120,
            placeholder="e.g. a cute banana astronaut on the moon, digital art",
        )

        negative_prompt = st.text_area(
            "Negative Prompt",
            value="",
            height=80,
            placeholder="things you do NOT want in the image",
        )

        steps = st.slider(
            "Steps",
            min_value=5,
            max_value=50,
            value=20,
            step=1
        )

        guidance = st.slider(
            "Guidance",
            min_value=1.0,
            max_value=15.0,
            value=7.5,
            step=0.5
        )

        width = st.slider(
            "Width",
            min_value=256,
            max_value=4096,
            value=512,
            step=64
        )

        height = st.slider(
            "Height",
            min_value=256,
            max_value=4096,
            value=512,
            step=64
        )

        seed = st.number_input(
            "Seed (-1 = random)",
            value=-1,
            step=1,
            format="%d"
        )

        generate_clicked = st.button(
            "Generate",
            type="primary",
            use_container_width=True
        )

    with col_right:
        st.subheader("Output")
        output_slot = st.empty()
        status_slot = st.empty()

    if generate_clicked:
        if not model_name:
            status_slot.error(
                "No model selected. Place a .safetensors file in models/checkpoints/."
            )
        elif not prompt or not prompt.strip():
            status_slot.error("Please enter a prompt.")
        else:
            with st.spinner("Generating..."):
                try:
                    image, out_path = _generate_image(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        model_name=model_name,
                        steps=steps,
                        guidance=guidance,
                        width=width,
                        height=height,
                        seed=int(seed),
                        low_vram=bool(low_vram),
                    )
                    output_slot.image(
                        image,
                        caption=out_path.name,
                        use_column_width=True
                    )
                    status_slot.success(f"Saved to {out_path}")
                except Exception as exc:
                    status_slot.error(f"Generation failed: {exc}")