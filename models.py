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
# Image-to-Image (Qwen Image Edit)
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

    def run(self, input_image, prompt: str, strength: float = 0.7, guidance_scale: float = 7.5):
        input_image = self._ensure_pil_image(input_image)

        with torch.inference_mode():
            result = self.pipe(
                prompt=prompt,
                image=input_image,
                strength=strength,
                guidance_scale=guidance_scale
            )

        def save_unique_image(output_image, save_dir, base_name="output_img2img.png"):
            """Save image and ensure unique filename like file explorer behavior."""
            name, ext = os.path.splitext(base_name)
            save_path = os.path.join(save_dir, base_name)
            counter = 2

            while os.path.exists(save_path):
                save_path = os.path.join(save_dir, f"{name}({counter}){ext}")
                counter += 1

            output_image.save(save_path)
            return save_path

        # Use the helper function
        output_image = result.images[0]
        save_path = save_unique_image(output_image, self.save_dir)

        return {"message": f"Img2Img generated at {save_path}", "image": output_image, "path": save_path}
# ---------------------------
# Model Handler
# ---------------------------

class ModelHandler:
    def __init__(self):
        self.text2img = TextToImageModel()
        self.img2img = ImageToImageModel()

    def run_model(self, *, prompt=None, input_image=None, strength=0.7, guidance_scale=7.5):
        if input_image and prompt:
            return self.img2img.run(
                input_image=input_image,
                prompt=prompt,
                strength=strength,
                guidance_scale=guidance_scale
            )
        elif prompt:
            return self.text2img.run(prompt=prompt)
        else:
            raise ValueError("You must provide a prompt, optionally an input_image for Img2Img.")
