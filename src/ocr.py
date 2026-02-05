import lmstudio as lms
import ollama
from ollama import chat
from ollama import ChatResponse
import os
import datetime
import log

def ocr_images_lmstudio():


    # Get the file name and location of all the images in the directory

    directory = "./output"

    images_to_process = [] # Array where all the files are stored

    for entry in os.scandir(directory):
        if entry.is_file():
            images_to_process.append(entry.path)

    # Load the model that will be used
    model = lms.llm("allenai/olmocr-2-7b")

    for current_file in images_to_process:
        image_path = current_file
        image_handle = lms.prepare_image(image_path)

        chat = lms.Chat()
        chat.add_user_message("Perform OCR on this image.", images=[image_handle])
        prediction = model.respond(chat)

        # Save the output as a .txt file
        prediction = str(prediction)

        file_name_only = os.path.basename(current_file)

        f = open(f"./output/text/{file_name_only}.txt", "w")
        f.write("\n")
        f.write(prediction)
        f.close()

def ocr_images_ollama():

    directory = "./output" # Set the directory where the outputted images will be located

    model_name = "deepseek-ocr:latest" # Set the model name

    images_to_process = [] # Array to store the variables in

    for entry in os.scandir(directory): # Loops the output diretory for the images to load
        if entry.is_file():
            images_to_process.append(entry.path)
    
    for current_file in images_to_process: # Loops through the images and proccesses them all individually

        try:
            response: ChatResponse = chat(
                model=model_name,
                messages=[
                {
                    'role': 'user', # Set the role of the api
                    'content': 'Free OCR.', # Prompt
                    'images': [current_file] # Select the image
                },
            ],
            options={
                'num_ctx':8000, # Set the context length
            }
            )
            file_name_only = os.path.basename(current_file)

            # Write the results to a .txt file named after the input
            f = open(f"./output/text/{file_name_only}.txt", "w")
            f.write("\n")
            f.write(response['message']['content'])
            f.close()

        except Exception as e:
            log(f"Failed to convert the following file: {current_file}.")
            continue

    chat(model=model_name, messages =[], keep_alive=0)