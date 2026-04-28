@echo off
echo ============================================
echo Starting Alpha Banana v1 (Streamlit)
echo ============================================

IF NOT EXIST banana_env (
    echo Environment not found.
    echo Please run install.bat first.
    pause
    exit
)

call banana_env\Scripts\activate

streamlit run streamlit_app.py

pause
