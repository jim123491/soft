import re
import requests
from bs4 import BeautifulSoup
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page as a string.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
    """
    # Wikipedia rejects requests without a User-Agent
    response = requests.get(url, headers={"User-Agent": "MLDS-week1-student/1.0"}, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The title of the page.
    """
    heading = soup.find("h1", id="firstHeading")
    return heading.get_text(strip=True) if heading else ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The first sentence of the first paragraph.
    """
    # Skip empty paragraphs (Wikipedia has a placeholder <p class="mw-empty-elt">)
    for p in soup.find_all("p"):
        text = re.sub(r"\s+", " ", re.sub(r"\[\d+\]", "", p.get_text())).strip()
        if text:
            match = re.match(r"(.+?[.!?])(\s|$)", text)
            return match.group(1) if match else text
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title of the page
        title = extract_title(soup)

        # Extract the first sentence of the first paragraph
        first_sentence = extract_first_sentence(soup)

        # Combine the extracted data
        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        # Print the extracted data
        print("Extracted Data:", extracted_data)

        # Save the data to a JSON file
        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
