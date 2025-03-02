from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
import torch


class SDImpainting:
    def __init__(self, device: str):
        self.pipe = AutoPipelineForInpainting.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1", torch_dtype=torch.float16, variant="fp16").to(device)

        self.generator = torch.Generator(device=device).manual_seed(0)

    def impaint(self, image_path: str, mask_path: str, prompt: str, negative_prompt: str, strength: float, guidance: float):
        image = load_image(image_path).resize((1024, 1024))
        mask_image = load_image(mask_path).resize((1024, 1024))

        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=image,
            mask_image=mask_image,
            guidance_scale=guidance,
            strength=strength,
            generator=self.generator,
        ).images[0]

        return image
