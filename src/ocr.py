import lmstudio as lms
import os
import datetime

def ocr_images():
    # Start the log with the date and time
    date_time = datetime.datetime.now() # Get the current date and time
    date_time = str(date_time) # Convert the date & time to a string
    
    # Get the file name and location of all the images in the directory

    directory = "./output"

    images_to_process = [] # Array where all the files are stored

    for entry in os.scandir(directory):
        if entry.is_file():
            images_to_process.append(entry.path)



    for current_file in images_to_process:
        image_path = current_file
        image_handle = lms.prepare_image(image_path)

        # Load the model that will be used
        model = "https://huggingface.co/lmstudio-community/olmOCR-2-7B-1025-GGUF@Q8_0"
        try:
          model = lms.llm(model)
        except lms.LMStudioError:
            print(f"Error: Make sure {model} is installed in LM Studio.")

            # Install model if not already installed
            print(f"Do you want to install {model} now? (y/n)") 
            answer = input()
            if answer.lower() == "y":
              os.system(f"lms get {model}")
            else:
               print("Exiting program.")
               quit()

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