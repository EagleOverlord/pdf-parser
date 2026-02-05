from log import *
initialise_log()

import pdf_to_image
import ocr
import os
import datetime
import time

log(f"Imports successfull at: {datetime.datetime.now()}")

os.makedirs("./input", exist_ok=True)
os.makedirs("./output", exist_ok=True)
os.makedirs("./output/text", exist_ok=True)

log(f"Created directories successfull at: {datetime.datetime.now()}")

image_conversion_start = time.time()
pdf_to_image.convert_pdf_to_images()
image_conversion_end = time.time()

log(f"Image conversion took: {image_conversion_end - image_conversion_start} seconds.")

model = ocr.choose_model() # Allow the user to choose the OCR model they wish to use.

ocr_start = time.time()
ocr.ocr_images_ollama(model)
ocr_end = time.time()

log(f"OCR conversion took: {ocr_end - ocr_start} seconds.")
log("Process completed.")
print(("Process completed."))