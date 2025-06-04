from diffusers import StableDiffusionPipeline
import torch

class ImageGenerator:
    def __init__(self, model_name="stabilityai/sd-turbo", use_gpu=False, cache_dir=None):
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.cache_dir = cache_dir

        print(f"[ImageGenerator] Chargement du modèle sur {self.device}...")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            cache_dir=self.cache_dir
        ).to(self.device)
        print("[ImageGenerator] Modèle prêt.")

    def generate(self, prompt: str, steps: int = 10):
        print(f"[ImageGenerator] Génération d'image pour : '{prompt}'")
        result = self.pipe(prompt, num_inference_steps=steps)
        image = result.images[0]
        image.show()
        return image
