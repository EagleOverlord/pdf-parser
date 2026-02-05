from openrouter import OpenRouter
import os
import lmstudio as lms
from ollama import chat
from ollama import ChatResponse

def summarise_ollama():
    # Open the .txt file
    files_to_process = [] # Stores the files that need processing in an array

    for entry in os.scandir("./output/text"): # Loops the output diretory for the images to load
        if entry.is_file():
            files_to_process.append(entry.path)

    for current_file in files_to_process:

        f = open(f"{current_file}")
        content_file = f.read() # Store the current file in a variable to be proccessed
        f.close()


        response: ChatResponse = chat(
            model='granite4:latest', # Able to select the model
            messages = [
                {
                    'role': 'user', # Adds the role 
                    # Prompt 
                    'content': f'Summarise the attached info - the user does not need the content repeating again {content_file}',
                },
        ],
        options={
            'num_ctx':32000, # Set the context length
        }
        )


        file_name_only = os.path.basename(current_file) # Avoid repeating

        f = open(f"./output/summarise/{file_name_only}.txt", "w")
        f.write(response['message']['content'])
        f.close()