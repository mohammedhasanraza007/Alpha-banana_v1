@echo off
echo ============================================
echo Alpha Banana v1 Installer
echo ============================================

IF EXIST banana_env (
    echo Virtual environment already exists.
    echo Skipping creation.
) ELSE (
    echo Creating virtual environment...
    python -m venv banana_env
)

call banana_env\Scripts\activate

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ============================================
echo Installation finished.
echo You only need to run this ONCE.
echo Next time use run.bat
echo ============================================
pause
