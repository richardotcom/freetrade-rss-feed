import argparse
import requests
import sys
from xml.etree import ElementTree as xml
from urllib.parse import urlparse

def group_urls_by_subdirectory(urls: list[str]) -> dict:
    grouped_urls = dict()

    for url in urls:
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split("/") if part]
        subdirectory = path_parts[0] if path_parts else "root"
        grouped_urls.setdefault(subdirectory, list()).append(url)

    return grouped_urls

def parse_sitemap(content: str):
    try:
        root = xml.fromstring(content)

        urls = list()

        for url_element in root.findall(".//{*}url"):
            loc_element = url_element.find(".//{*}loc")
            if loc_element is not None:
                urls.append(loc_element.text)

        grouped_urls = group_urls_by_subdirectory(urls)

        for subdirectory, urls_containing_subdirectory in grouped_urls.items():
            print(f"{subdirectory}: {len(urls_containing_subdirectory)}")
    except xml.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path or URL to sitemap")
    args = parser.parse_args()
    source = args.source

    try:
        parsed_url = urlparse(source)
        if parsed_url.scheme and parsed_url.netloc:
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
