from pdf2image import convert_from_path, convert_from_bytes
import os
import datetime

def convert_pdf_to_images():

    # Variables for where the directories will be located
    input_directory = r"./input"

    # Array to store the .pdf locations in
    pdfs_to_process = []

    # Find all the pdfs to process w/ error handling
    try:
      for entry in os.scandir(input_directory):
                
        if entry.is_file():
                pdfs_to_process.append(entry.path)
    except FileNotFoundError:
        print("Error: Valid input directory was not found.")
        return

    
    for current_file in pdfs_to_process:

        clean_name = os.path.splitext(os.path.basename(current_file))[0]

        images = convert_from_path(current_file)

        for i, image in enumerate(images):
            file_name = f"./output/{clean_name}page_{i}.jpg"
            
            image.save(file_name, "JPEG")

