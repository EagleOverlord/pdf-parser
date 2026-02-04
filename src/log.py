import os
import datetime

def initialise_log():
    # Initialise the log file

    os.makedirs("./log", exist_ok=True)

    current_datetime = datetime.datetime.now()

    f = open("./log/log.txt", "w")
    f.write("****************\n")
    f.write(f"The process started at: {current_datetime} \n")
    f.close()

def log_moment(event):
    
    f = open("./log/log.txt", "a")
    f.write(f"{event} \n")
    f.close()