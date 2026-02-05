import os
from ollama import ResponseError, chat
from ollama import ChatResponse
import get_settings
from log import *

def summarise_ollama():

    model_name = get_settings.gs('sum_model_name')

    # Open the .txt file
    files_to_process = [] # Stores the files that need processing in an array

    for entry in os.scandir("./output/text"): # Loops the output diretory for the images to load
        if entry.is_file():
            files_to_process.append(entry.path)

    for current_file in files_to_process:

        f = open(f"{current_file}")
        content_file = f.read() # Store the current file in a variable to be proccessed
        f.close()

        try:


            response: ChatResponse = chat(
                model=get_settings.gs('sum_model_name'), # Able to select the model
                messages = [
                    {
                        'role': 'user', # Adds the role 
                        # Prompt 
                        'content': f'Summarise the attached info - the user does not need the content repeating again {content_file}',
                    },
            ],
            options={
                'num_ctx':int(get_settings.gs('sum_context_length')), # Set the context length
            }
            )


            file_name_only = os.path.basename(current_file) # Avoid repeating

            f = open(f"./output/summarise/{file_name_only}.txt", "w")
            f.write(response['message']['content'])
            f.close()

            print(f"Completed summary on {current_file}")
        except ResponseError as e:
                log(f"Failed to summarise {current_file} - file not found. Error: {e} \n Asking user if they wish to install {model_name}")
                user_input = input(f"Model {model_name} not found. Do you wish to install it? (y/n): ")
                if user_input.lower() == 'y':
                    os.system(f"ollama pull {model_name}") # Pull the model if not found
                    log(f"Model {model_name} installed successfully. Retrying summarisation for {current_file}.")
                    summarise_ollama() # Retry the summarisation after installing the model
                else:
                    log(f"User chose not to install {model_name}. Skipping summarisation.")
                    print("Summarisation skipped..")
        else:
            log(f"Error summarising {current_file}")
