import os
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from torchvision import transforms

# ---------------------------
# Base Model
# ---------------------------
class BaseModel:
    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

# ---------------------------
# Text-to-Image (Stable Diffusion)
# ---------------------------
class TextToImageModel(BaseModel):
    def __init__(self, save_dir="Data"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        model_id = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            self.pipe = self.pipe.to("cuda")

    def run(self, prompt: str):
        image = self.pipe(prompt).images[0]
        save_path = os.path.join(self.save_dir, f"{prompt.replace(' ', '_')}.png")
        image.save(save_path)
        return {"message": f"Text-to-Image generated at {save_path}", "image": image, "path": save_path}

# ---------------------------
# Image-to-Image (Stable Diffusion)
# ---------------------------
class ImageToImageModel(BaseModel):
    def __init__(self, save_dir="Data"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        model_id = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            self.pipe = self.pipe.to("cuda")

    def _ensure_pil_image(self, input_image):
        """Convert input to a valid PIL.Image.Image"""
        if isinstance(input_image, Image.Image):
            return input_image.convert("RGB")
        elif isinstance(input_image, str):
            return Image.open(input_image).convert("RGB")
        elif isinstance(input_image, torch.Tensor):
            to_pil = transforms.ToPILImage()
            return to_pil(input_image.cpu()).convert("RGB")
        elif hasattr(input_image, "__array__"):  # numpy array
            to_pil = transforms.ToPILImage()
            return to_pil(input_image).convert("RGB")
        else:
            raise TypeError(
                f"Unsupported input_image type: {type(input_image)}. "
                "Must be PIL.Image, numpy.ndarray, torch.Tensor, or file path string."
            )