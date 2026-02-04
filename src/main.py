import pdf_to_image
import ocr
import os 

os.makedirs("./output", exist_ok=True)
os.makedirs("./output/text", exist_ok=True)

pdf_to_image.convert_pdf_to_images()

ocr.ocr_images()