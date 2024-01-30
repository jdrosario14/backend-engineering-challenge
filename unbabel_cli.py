"""Unbabel Backend Engineering Challenge Client"""
import os
import json
from datetime import datetime
from argparse import ArgumentParser
from moving_average_calculator import moving_average


def main():
    """
    Main function for processing input data and calculating moving averages.

    This function performs the following steps:
    1. Parses command-line arguments using `parse_args`.
    2. Validates the parsed arguments using `validate_args`.
    3. Reads and processes input data from a JSON file using `handle_input_file`.
    4. Calculates moving averages based on the processed data using `moving_average`.
    5. Writes the result list to a JSON file inside the "outputs" directory.
    6. Prints a message indicating the location of the result file.

    Usage:
    - Execute this function to process input data and generate moving averages.

    Command-line arguments:
    - --input_file (str): The path to the JSON file containing input data.
    - --window_size (int): The size of the window for calculating moving averages.
    """

    args = parse_args()
    input_file = args.input_file
    window_size = args.window_size

    validate_args(input_file, window_size)
    events = handle_input_file(input_file)
    moving_avg_results = moving_average(events, window_size)

    # Write the result list to a JSON file inside the "outputs" directory
    file_name = f"{os.path.splitext(os.path.basename(input_file))[0]}_{window_size}"
    with open(f"outputs/{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(moving_avg_results, json_file, indent=2)

    print(f"The result can be found in outputs/{file_name}.json")


def parse_args():
    """
    Parses the command-line arguments.

    Returns:
    - argparse.Namespace: An object containing the parsed arguments.
    """

    parser = ArgumentParser(description="Process events from a JSON file.")
    parser.add_argument(
        "--input_file", type=str, required=True, help="Path to the input JSON file."
    )
    parser.add_argument(
        "--window_size", type=int, required=True, help="Size of the window (integer)."
    )

    return parser.parse_args()


def validate_args(input_file, window_size):
    """
    Validates the input values.

    Parameters:
    - input_file (str): The path of the input file containing the events.
    - window_size (int): The size of the window in minutes.

    Raises:
    - ValueError: If the window_size is not an integer greater than 0.
    - FileNotFoundError: If the input_file is not a valid path of an existent file.
    """

    if window_size <= 0:
        raise ValueError("The window size must be an integer greater than 0.")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file '{input_file}' does not exist.")


def handle_input_file(input_file):
    """
    Reads a JSON file, extracts information, and returns a list of objects.

    Parameters:
    - input_file (str): The path to the JSON file containing data.

    Returns:
    - List[dict]: A list of dictionaries with "datetime" (converted timestamp string to datetime
      object) and "duration". Each dictionary corresponds to an entry in the input file.

    Raises:
    - ValueError: If the JSON file is empty.
    """

    # Reads the JSON file and loads it to the data variable
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if len(data) == 0:
        raise ValueError("The JSON file is empty.")

    # Returns a new list of objects with "datetime" (converted timestamp string to datetime
    # object) and "duration"
    return [
        {
            "datetime": datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
            "duration": entry["duration"],
        }
        for entry in data
    ]


if __name__ == "__main__":
    main()
