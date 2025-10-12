# modules/scene_locator.py
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load once globally for performance
model = None
processor = None
landmarks = [
    "Eiffel Tower, Paris",
    "Times Square, New York",
    "Lagos Market, Nigeria",
    "Burj Khalifa, Dubai",
    "London Bridge, UK",
    "Taj Mahal, India",
    "Sydney Opera House, Australia",
]

def _ensure_model_loaded():
    global model, processor
    if model is None:
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def match_scene_location(image_path):
    """Compare image embedding to known landmark embeddings using CLIP."""
    _ensure_model_loaded()
    image = Image.open(image_path)
    inputs = processor(text=landmarks, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)[0]
    best_idx = torch.argmax(probs).item()
    return {"guess": landmarks[best_idx], "confidence": float(probs[best_idx])}
