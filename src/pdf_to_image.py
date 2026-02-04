from pdf2image import convert_from_path, convert_from_bytes
import os
import datetime

def convert_pdf_to_images():

    os.makedirs("./output", exist_ok=True)

    images = convert_from_path("./input/sample.pdf")

    for i, image in enumerate(images):
        file_name = f"./output/page_{i}.jpg"
        
        image.save(file_name, "JPEG")

convert_pdf_to_images()