import argparse
import requests
import sys
from xml.etree import ElementTree as xml

def parse_sitemap(content: str):
    try:
        root = xml.fromstring(content)

        for url_element in root.findall(".//{*}url"):
            loc_element = url_element.find(".//{*}loc")
            if loc_element is not None:
                print(loc_element.text)
    except xml.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path or URL to sitemap")
    args = parser.parse_args()
    source = args.source

    try:
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            content = response.text
        else:
            with open(source, "r") as file:
                content = file.read()

        parse_sitemap(content)
    except requests.RequestException as e:
        print(f"Error fetching sitemap from \"{source}\": {e}", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as e:
        print(f"Failed to read file \"{source}\": {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
