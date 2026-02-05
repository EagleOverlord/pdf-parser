import lmstudio as lms
from ollama import chat
from ollama import ChatResponse
import os
import datetime
import log


# Set the settings for the program
output_directory = "./output"
file_format = ".txt"

def save_output(content,file_name):

    file_name_only = os.path.basename(file_name)

    if file_format == ".txt":
        f = open(f"./output/text/{file_name_only}{file_format}","w")
        f.write(content)
        f.close()
    else:
        print("Not a valid file format")
        quit()

def ocr_images_lmstudio():
    images_to_process = [] # Array where all the files are stored

    for entry in os.scandir(output_directory):
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

    images_to_process = [] # Array to store the variables in

    for entry in os.scandir(output_directory): # Loops the output diretory for the images to load
        if entry.is_file():
            images_to_process.append(entry.path)
    
    for current_file in images_to_process: # Loops through the images and proccesses them all individually

        try:
            response: ChatResponse = chat(
                model='deepseek-ocr:latest',
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

            save_output(response['message']['content'],current_file)
            print(f"Completed file {current_file}")
            log.log(f"Completed file {current_file}")

        except Exception as e:
            log.log(f"Failed to OCR the following file {current_file}. Error {e}")

    chat(model='qwen3-vl:8b', messages =[], keep_alive=0)