import requests
import logging
from html.parser import HTMLParser
import html

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
)


async def fetch_page_content(url: str) -> tuple:
    """
    Fetches the content of a webpage along with its headers.

    :param url: URL of the webpage to fetch.
    :return: Tuple containing HTML content as a string and response headers, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Determine the encoding from headers or default to UTF-8
        encoding = response.encoding if response.encoding else "utf-8"
        content = response.content.decode(encoding)
        return content, response.headers
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None, None


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_with_tags = []
        self.current_tags = []
        self.ignore_tags = {'script', 'meta', 'link', 'svg', 'path'}  # Add more tags as needed
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        if tag in self.ignore_tags:
            self.skip_content = True
        else:
            self.current_tags.append(tag)
            self.text_with_tags.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.skip_content = False
        else:
            self.current_tags.pop()
            self.text_with_tags.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip_content and data.strip():
            self.text_with_tags.append(html.escape(data))

async def extract_text_from_html(html_content):
    parser = MyHTMLParser()
    parser.feed(html_content)
    return ''.join(parser.text_with_tags)
