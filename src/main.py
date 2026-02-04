import log

log.initialise_log()

import pdf_to_image
import ocr
import os
import datetime
import time

log.log_moment(f"Imports successfull at: {datetime.datetime.now()}")

os.makedirs("./input", exist_ok=True)
os.makedirs("./output", exist_ok=True)
os.makedirs("./output/text", exist_ok=True)

log.log_moment(f"Created directories successfull at: {datetime.datetime.now()}")

image_conversion_start = time.time()
pdf_to_image.convert_pdf_to_images()
image_conversion_end = time.time()

log.log_moment(f"Image conversion took: {image_conversion_end - image_conversion_start} seconds.")

ocr_start = time.time()
ocr.ocr_images_ollama()
ocr_end = time.time()

log.log_moment(f"OCR conversion took: {ocr_end - ocr_start} seconds.")