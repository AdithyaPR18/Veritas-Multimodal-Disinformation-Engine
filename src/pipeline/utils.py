import easyocr
import numpy as np
from PIL import Image

# Initialize the reader once to avoid reloading overhead
# In a real production system, this might be a separate service or loaded in the consumer initialization
reader = easyocr.Reader(['en'], gpu=False) # Set gpu=True if CUDA/MPS available and configured

def ocr_check(image_path, headline):
    """
    Performs a secondary check using OCR.
    If text in the image strongly contradicts or is irrelevant to the headline, 
    this flags it. For this MVP, we just return the detected text and a simple flag 
    if any keyword from the headline appears in the image text (authenticity check).
    """
    try:
        result = reader.readtext(image_path)
        detected_text = " ".join([res[1] for res in result])
        
        # Simple heuristic: Check if any significant word from headline is in the image
        # This is a placeholder for "Semantic Mismatch" logic via OCR.
        # In a real system, you'd check for CONTRADICTIONS, not just overlap.
        
        headline_words = set(headline.lower().split())
        image_words = set(detected_text.lower().split())
        
        common_words = headline_words.intersection(image_words)
        
        # If we find common words, maybe it's authentic? 
        # Or if we find NO common words, maybe it's suspicious?
        # For the "uncertainty" logic, we just return the data for the consumer to log.
        
        return {
            "triggered": True,
            "detected_text": detected_text,
            "common_words": list(common_words)
        }
    except Exception as e:
        print(f"OCR Failed: {e}")
        return {"triggered": True, "error": str(e)}
