"""
// test_microservice.py
This is a test program to verify the functionality of the
pdf generator microservice
"""

import json
import requests
import os


# JSON Data File must be in same folder
DEFAULT_FILENAME = "records.json"  # CHANGE THIS FILE NAME AS NEEDED


def get_data_file():
    """
    Function to find JSON data file
    """
    # Find the folder where *this script* lives
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Define the absolute path to the JSON file
    default_path = os.path.join(script_directory, DEFAULT_FILENAME)

    # If it exists, use it; otherwise fall back to a prompt
    if os.path.isfile(default_path):
        return default_path

    # Otherwise ask the user (and expand ~ if they type it)
    user_path = input(
        f"Default data not found at {default_path!r}.\n"
        "Enter full path to your JSON data file: "
    ).strip()
    user_path = os.path.expanduser(user_path)
    if not os.path.isfile(user_path):
        raise FileNotFoundError(f"No file at {user_path}")
    return user_path


def main():
    """
    Finds and loads JSON data, constructs payload with folder, filename, and records;
    Sends POST request to PDF microservice and confirms success or error message.
    """
    data_file = get_data_file()

    with open(data_file, "r") as file:
        records = json.load(file)

    # Set output save folder and desired pdf file name
    folder = os.getcwd()  # Currently set to save to current working directory
    name = "maintenance_report.pdf"

    payload = {
        "folder": folder,
        "filename": name,
        "records": records
    }

    # Check POST response status
    response = requests.post("http://127.0.0.1:8000/generate", json=payload)
    if response.status_code == 200 and response.json().get("status") == "success":
        print("PDF saved at", response.json()["path"])
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()
