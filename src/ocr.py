import lmstudio as lms
import ollama
from ollama import ResponseError, chat
from ollama import ChatResponse
import os
import datetime
from log import *
import requests

def ocr_images_lmstudio():


    # Get the file name and location of all the images in the directory

    directory = "./output"

    images_to_process = [] # Array where all the files are stored

    for entry in os.scandir(directory):
        if entry.is_file():
            images_to_process.append(entry.path)

    # Load the model that will be used
    model = lms.llm("allenai/olmocr-2-7b") # This imports the wrong quantization, I'll fix it in a bit

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

def ocr_images_ollama(model_name):

    directory = "./output" # Set the directory where the outputted images will be located

    log(f"Using model: {model_name}.")

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

<<<<<<< HEAD
        except Exception as e:
            log(f"Failed to convert the following file: {current_file}.")
            continue
=======
        # Write the results to a .txt file named after the input
        f = open(f"./output/text/{file_name_only}.txt", "w")
        f.write("\n")
        f.write(response['message']['content'])
        f.close()
        log(f"Finished: {current_file}.")
>>>>>>> 0072df8522f69d6126c7279e5f17397f426ed11e


    chat(model=model_name, messages =[], keep_alive=0)

def choose_model():

    # Hashmap of supported LLM models, there's probably a better way to do this

    models = {1:"deepseek-ocr:latest", 
              2:"qwen3-vl:8b",
              } 

    print("Pick an AI model to use for OCR. The following models are supported:")
    for model_num, model_name in models.items():
        print(f"{model_num}. {model_name}")
    choice = int(input("Enter the number of the model you want to use: "))
    if choice in models:
        model_name = models[choice]
        os.system(f"ollama pull {model_name}")
    else:
        print("Invalid choice, defaulting to deepseek-ocr:latest")
        model_name = "deepseek-ocr:latest"


    return model_name