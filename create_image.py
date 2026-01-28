# Helper script to create an image, though producer.py handles it too.
# I will just rely on producer.py to create it.
# Actually, I'll create it here to be sure.
from PIL import Image, ImageDraw

img = Image.new('RGB', (224, 224), color = (73, 109, 137))
d = ImageDraw.Draw(img)
d.text((10,10), "Veritas Test Image", fill=(255,255,0))
img.save("test_image.jpg")
