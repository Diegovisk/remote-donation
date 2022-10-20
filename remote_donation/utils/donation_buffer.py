import os
import json
from dataclasses import dataclass

FILE_NAME = "offline_buffer.json"

@dataclass
class OfflineDonation:
    name: str
    time: int

def create_donation_buffer_if_not_exists():
    if not os.path.exists(FILE_NAME):
        clear_buffer()

# After connection is established
def get_buffer():
    create_donation_buffer_if_not_exists()
    file = open(FILE_NAME, "r")
    file_content = file.read()
    buffer = []
    for donation in json.loads(file_content):
        buffer.append(
            OfflineDonation(donation["name"], donation["time"])
        )
    file.close()
    return buffer

# If all files were OK
def clear_buffer():
    file = open(FILE_NAME, "w")
    file.write("[]")
    file.close()

# write to file
def write_buffer(data):
    create_donation_buffer_if_not_exists()
    for i in range(len(data)):
        print(data[i])
        data[i] = {
            "name": data[i].name,
            "time": data[i].time
        }
        
    serialized_data = json.dumps(data)
    file = open(FILE_NAME,"w")
    file.write(serialized_data)
    file.close()

# Append if failed connection
def append_buffer(donation: OfflineDonation):
    create_donation_buffer_if_not_exists()
    buffer = get_buffer()
    buffer.append(donation)
    write_buffer(buffer)