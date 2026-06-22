# This program pulls text directly from the UP Mindanao related websites and uses the libraries BeautifulSoup and Requests to scrape the content. The scraped text is then cleaned and formatted for use in the chatbot's knowledge base. This allows the chatbot to provide accurate and up-to-date information about UP Mindanao based on the content available on the official website.


# BeautifulSoup is used for parsing HTML content and extracting readable text from web pages.
# Web scraping is done in 4 steps:
# 1. Send an HTTP request to the target URL and get the HTML content which uses the Requests library.
# 2. Use BeautifulSoup to parse the HTML and navigate the DOM tree to easily navigate and extract specific parts of the content.
# 3. Remove unwanted or filter elements like scripts, styles, navigation bars, and footers to focus on the main content.
# 4. Extract the text, clean it up by removing excessive whitespace, and format it for output.
# The scraped text is then combined and can be used for further processing, such as feeding into an AI model for question-answering or summarization tasks.

# scraper.py
import requests
from bs4 import BeautifulSoup


# Pages from UP Mindanao website to scrape
PAGES_TO_SCRAPE = [
    {
        "label": "UP Mindanao Homepage",
        "url"  : "https://www.upmin.edu.ph"
    },
    {
        "label": "About UP Mindanao - Organization Chart", # This page is only an image, so it may not yield much text content.
        "url"  : "https://upmin.edu.ph/about-us/organization/"
    },
    {
        "label": "About UP Mindanao - Officials",
        "url"  : "https://upmin.edu.ph/about-us/administration/"
    },
    {
        "label": "About UP Mindanao - UP Quality Policy",
        "url"  : "https://upmin.edu.ph/about-us/upqualitypolicy/"
    },
    {
        "label": "UP Mindanao - Academic Programs",
        "url"  : "https://upmin.edu.ph/academics/academic-programs/"
    },
]

def scrape_page(label, url):
    """Scrape readable text from a single webpage."""
    try:
        print(f"  Scraping: {label}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove navigation, scripts, and footer clutter
        for tag in soup(["script", "style", "nav", "footer",
                          "header", "aside", "form"]):
            tag.decompose()

        # Extract clean text
        text = soup.get_text(separator="\n")

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines()]
        clean_lines = [line for line in lines if len(line) > 30]
        clean_text = "\n".join(clean_lines)

        return f"=== {label.upper()} ===\nSource: {url}\n\n{clean_text}\n"

    except requests.exceptions.RequestException as e:
        print(f"  Could not scrape {url}: {e}")
        return f"=== {label.upper()} ===\n[Could not load — page unavailable]\n"


def scrape_all():
    """Scrape all pages and return combined text."""
    print("\n Scraping UP Mindanao website...")
    all_text = []
    for page in PAGES_TO_SCRAPE:
        text = scrape_page(page["label"], page["url"])
        all_text.append(text)
    print("  Website scraping complete.\n")
    return "\n".join(all_text)


# Run standalone to test
if __name__ == "__main__":
    result = scrape_all()
    print(result[:2000])   # preview first 2000 characters