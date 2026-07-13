import requests
import sys
from xml.etree import ElementTree as xml

def main():
    try:
        response = requests.get("https://freetrade.io/sitemap.xml")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}", file=sys.stderr)
        sys.exit(1)
 
    try:
        root = xml.fromstring(response.content)
    except xml.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)

    NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for child in root:
        url_element = child.find("sm:loc", NS)
        if url_element is not None:
            print(url_element.text)

if __name__ == "__main__":
    main()
