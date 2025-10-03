# AI Image Generator GUI

This project is a desktop application built with Tkinter that allows you to generate images using Stable Diffusion models. It supports:

1. Text-to-Image generation
2. Image-to-Image (editing existing images using prompts)

---

## Files

- `main.py`     : Entry point for the application. Creates the Tk root window and runs the GUI.
- `gui.py`      : Contains the `AIApp` class that defines the GUI interface.
- `models.py`   : Contains `ModelHandler`, `TextToImageModel`, and `ImageToImageModel`.

---

## Features

- Input text to generate images or modify existing images.
- Image preview in the GUI.
- Automatic saving of outputs to a `Data/` folder.
- Duplicate filenames are handled automatically (e.g., `output_img2img(2).png`).
- Displays model information and optional OOP explanation in the interface.

---

## Requirements

- **Python 3.11 or 3.12** (⚠️ `torchvision` does not currently support Python 3.13+)
- Install dependencies:

    pip install -r requirements.txt

---

## Notes

- This project requires `torch`, `torchvision`, and `diffusers`.
- ⚠️ **Python 3.13 is not supported** because `torchvision` does not yet provide wheels for it.  
  Please create a virtual environment with Python **3.12** (recommended) or **3.11**.
- Example (using Conda):

    ```bash
    conda create -n ai_env python=3.12
    conda activate ai_env
    pip install -r requirements.txt
    ```

- GPU is recommended for faster generation.  
- Ensure your system has CUDA if using GPU acceleration.  

## Usage

1. Run the application via `main.py`:

    python main.py

2. The GUI window will open.  
3. Select a model: "Text-to-Image" or "Image-to-Image".  
4. Enter a prompt in the input section.  
5. For Image-to-Image, click "Browse" to select an input image.  
6. Click "Generate" to produce the image.  
7. Generated images will be saved in the `Data/` folder, with automatic renaming if a file already exists.

---

## Author

- Developed using Python, PyTorch, and Hugging Face Diffusers.
