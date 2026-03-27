from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

class VLM:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def generate_description(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt")
        out = self.model.generate(**inputs, max_new_tokens=40, num_beams=5)

        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption