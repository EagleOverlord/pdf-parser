import lmstudio as lms
from ollama import chat
from ollama import ChatResponse
import os
import datetime
import log
import get_settings

def save_output(content,file_name):

    # Retrieve the file_format from the .ini config
    file_format = get_settings.gs('ocr_file_format')

    file_name_only = os.path.basename(file_name)

    if file_format == ".txt":
        f = open(f"./output/text/{file_name_only}{file_format}","w")
        f.write(content)
        f.close()
    else:
        print("Not a valid file format")
        quit()

def ocr_images():

    images_to_process = [] # Array to store the variables in

    for entry in os.scandir(get_settings.gs('ocr_output_directory')): # Loops the output diretory for the images to load
        if entry.is_file():
            images_to_process.append(entry.path)
    
    for current_file in images_to_process: # Loops through the images and proccesses them all individually

        try:
            response: ChatResponse = chat(
                model=get_settings.gs('ocr_model_name'), # Get the model from the .ini file
                messages=[
                    {
                        'role': 'user', # Set the role of the api
                        'content': 'Free OCR.', # Prompt
                        'images': [current_file] # Select the image
                    },
            ],
            options={
                'num_ctx':int(get_settings.gs('ocr_context_length')), # Set the context length
            }
            )

            save_output(response['message']['content'],current_file)
            print(f"Completed OCR on {current_file}")
            log.log(f"Completed file {current_file}")

        except Exception as e:
            log.log(f"Failed to OCR the following file {current_file}. Error {e}")

    chat(model=get_settings.gs('ocr_model_name'), messages =[], keep_alive=0)