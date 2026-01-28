import torch
from src.models.veritas_model import VeritasNet
from src.pipeline.utils import ocr_check
from transformers import BertTokenizer
from torchvision import transforms
from PIL import Image
import os

def run_demo():
    print("=== Veritas Local Demo ===")
    
    # 1. Setup Model
    print("Initializing Model...")
    model = VeritasNet()
    model.eval()
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    image_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    # 2. Setup Data
    headline = "BREAKING NEWS: Aliens land in New York City"
    image_path = "test_image.jpg"
    
    if not os.path.exists(image_path):
        print("Creating dummy image...")
        from PIL import ImageDraw
        img = Image.new('RGB', (224, 224), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), "BREAKING NEWS", fill=(255,255,0))
        img.save(image_path)
    
    print(f"Testing on Headline: '{headline}'")
    print(f"Testing on Image: {image_path}")
    
    # 3. Model Inference
    inputs = tokenizer(headline, return_tensors='pt', padding=True, truncation=True, max_length=64)
    image = Image.open(image_path).convert('RGB')
    image_tensor = image_transforms(image).unsqueeze(0)
    
    print("Running Forward Pass...")
    with torch.no_grad():
        score = model(inputs['input_ids'], inputs['attention_mask'], image_tensor).item()
    
    print(f"Authenticity Score: {score:.4f}")
    
    # 4. OCR Check
    print("Running OCR Check...")
    ocr_result = ocr_check(image_path, headline)
    print(f"OCR Result: {ocr_result}")
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    run_demo()
