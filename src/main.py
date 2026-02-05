import log

log.initialise_log()

import pdf_to_image
import ocr
import os
import datetime
import time
import summarise

log.log(f"Imports successfull at: {datetime.datetime.now()}")

os.makedirs("./input", exist_ok=True)
os.makedirs("./output", exist_ok=True)
os.makedirs("./output/text", exist_ok=True)
os.makedirs("./output/summarise", exist_ok=True)

log.log(f"Created directories successfull at: {datetime.datetime.now()}")

image_conversion_start = time.time()
pdf_to_image.convert_pdf_to_images()
image_conversion_end = time.time()

log.log(f"Image conversion took: {image_conversion_end - image_conversion_start} seconds.")

ocr_start = time.time()
ocr.ocr_images()
ocr_end = time.time()

log.log(f"OCR conversion took: {ocr_end - ocr_start} seconds.")

summarise_start = time.time()
summarise.summarise_ollama()
summarise_end = time.time()

log.log(f"Summarisation took: {summarise_end - summarise_start} seconds.")