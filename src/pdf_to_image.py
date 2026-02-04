from pdf2image import convert_from_path, convert_from_bytes
import os
import datetime

def convert_pdf_to_images():

    # Variables for where the directories will be located
    input_directory = "./input"

    # Array to store the .pdf locations in
    pdfs_to_process = []

    # Find all the pdfs to process
    for entry in os.scandir(input_directory):
        if entry.is_file():
            pdfs_to_process.append(entry.path)
    
    for current_file in pdfs_to_process:

        clean_name = os.path.splitext(os.path.basename(current_file))[0]

        images = convert_from_path(current_file)

        for i, image in enumerate(images):
            file_name = f"./output/{clean_name}page_{i}.jpg"
            
            image.save(file_name, "JPEG")

