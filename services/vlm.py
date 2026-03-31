from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

class VLM:
    def __init__(self):
        print("--- Initializing Drone Vision System ---")
        # Load the processor and model once during initialization to save memory
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def generate_description(self, image_path: str) -> str:
        """
        Generates a natural language description of the image at the given path.
        Includes safety checks for missing or corrupted files.
        """
        
        # 1. Safety Check: Does the file actually exist?
        if not os.path.exists(image_path):
            import logging
            logging.error(f"Image not found at: {image_path}")
            return "error: missing_file"

        # 2. Process Image with Error Handling
        try:
            # Open and convert image to RGB (Standard for BLIP)
            image = Image.open(image_path).convert('RGB')
            
            # Prepare inputs for the BLIP model
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Generate the caption
            # num_beams=5 provides higher quality, descriptive results
            out = self.model.generate(
                **inputs, 
                max_new_tokens=40, 
                num_beams=5
            )
            
            # Decode the output into a clean string
            description = self.processor.decode(out[0], skip_special_tokens=True)
            
            return description

        except Exception as e:
            # Catches corrupted images, file format errors, or hardware issues
            print(f"[VLM CRASH] Could not process image: {e}")
            return f"error: {str(e)}"

# Example Usage:
# vision_system = VLM()
# print(vision_system.generate_description("data/images/truck.jpg"))