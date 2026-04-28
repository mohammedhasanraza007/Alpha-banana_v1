
#Alpha-Banana_v1 🍌

#Overview
Alpha Banana v1 is a tool that helps you create images using AI on your own computer. It uses Stable Diffusion and Streamlit to make this possible. The main advantage is that it works fully offline after setup, keeping everything local on your machine. It is designed to be easy to install, beginner-friendly, and compatible with different hardware setups.
#Features
- Create images from text using Stable Diffusion
- Automatically downloads the required model on first run (~3–4GB)
- Works with CPU if no GPU is available
- Supports NVIDIA GPUs with CUDA for faster performance
- Simple web-based UI using Streamlit
- Allows custom models via models/checkpoints folder
System Requirements
#Minimum:
- Windows 10 or 11
- 8GB RAM
- CPU support (slower performance)

#Recommended:
- NVIDIA GPU with CUDA support
- 16GB RAM or more
- SSD storage for faster loading
#Important Notes
- Windows only (no Linux/macOS support yet)
- First launch downloads model (~3–4GB)
- Do not close app during first run
- First run may take 10–20 minutes depending on system and internet
#How It Works
On first run, the system downloads the Stable Diffusion model from Hugging Face and stores it locally. After that, the model is reused. The system automatically detects hardware and uses GPU if available, otherwise falls back to CPU.
#Installation Steps
#Step 1: Download or clone repository
#Step 2: Run install.bat to install dependencies
#Step 3: Launch using run_streamlit.bat
#Step 4: Wait for first model download
#Step 5: Open localhost in browser
#Model System
Uses Stable Diffusion v1.5 EMA-pruned model. Automatically downloaded on first run. Users can add custom models inside models/checkpoints folder.
#Contributions
Solo developer project. Contributions and suggestions are welcome. Future updates may include image-to-image generation, better GPU optimization, and UI improvements.
#License
#MIT License
