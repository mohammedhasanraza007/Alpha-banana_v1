"""
streamlit_app.py
----------------
Entry point for Alpha Banana v1 (Streamlit edition).

Run with:
    streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from streamlit_ui import render_ui


def main():
    render_ui()


if __name__ == "__main__":
    main()
else:
    main()
