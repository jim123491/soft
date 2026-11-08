import csv
import re
from typing import List, Dict

# Operates on cleaned (ASCII-only) text, so the degree sign is already gone
LINE_RE = re.compile(
    r"Date:\s*(?P<date>\d{4}-\d{2}-\d{2}),\s*"
    r"Max Temp:\s*(?P<max>-?\d+(?:\.\d+)?)\s*C,\s*"
    r"Min Temp:\s*(?P<min>-?\d+(?:\.\d+)?)\s*C,\s*"
    r"Humidity:\s*(?P<hum>\d+)\s*%,\s*"
    r"Precipitation:\s*(?P<prec>\d+(?:\.\d+)?)\s*mm"
)


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    line = line.replace("\u00a0", " ")
    return line.encode("ascii", "ignore").decode("ascii").strip()


def extract_weather_data(text_file: str) -> List[Dict[str, any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    with open(text_file, encoding="utf-8") as f:
        lines = f.readlines()
    data = []
    for line in lines:
        match = LINE_RE.search(clean_text(line))
        if match:
            data.append({
                "date": match["date"],
                "max_temperature": float(match["max"]),
                "min_temperature": float(match["min"]),
                "humidity": int(match["hum"]),
                "precipitation": float(match["prec"]),
            })
    return data


def save_to_csv(data: List[Dict[str, any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    keys = ["date", "max_temperature", "min_temperature", "humidity", "precipitation"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for d in data:
            writer.writerow([d[k] for k in keys])


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
