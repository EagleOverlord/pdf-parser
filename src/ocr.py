import lmstudio as lms
from ollama import chat
from ollama import ChatResponse
import os
import datetime

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

    directory = "./output"

    images_to_process = []

    for entry in os.scandir(directory):
        if entry.is_file():
            images_to_process.append(entry.path)
    
    for current_file in images_to_process:
        response: ChatResponse = chat(model='qwen3-vl:8b', messages=[
        {
            'role': 'user',
            'content': 'OCR this image.',
            'images': [current_file]
        },
        ])
        options={
            'num_ctx':20000,
        }

        file_name_only = os.path.basename(current_file)

        f = open(f"./output/text/{file_name_only}.txt", "w")
        f.write("\n")
        f.write(response['message']['content'])
        f.close()

ocr_images_ollama()