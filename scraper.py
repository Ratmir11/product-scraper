import argparse
import csv
import json
import time

from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")

OUTPUT_DIR = Path("output")

MAX_ATTEMPTS = 3
REQUEST_TIMEOUT = 10
RETRY_DELAY = 2


def get_page(url):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            response.encoding = "utf-8"
            return response.text

        except requests.RequestException as ex:
            print(f"Attempt {attempt}/{MAX_ATTEMPTS} failed: {ex}")

            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY)

    raise RuntimeError(f"Failed to fetch page: {url}")


def parse_books(html, page_url):
    soup = BeautifulSoup(html, "lxml")

    articles = soup.select("article.product_pod")
    books = []

    for article in articles:
        link = article.select_one("h3 a")

        title = link["title"]
        price = article.select_one(".price_color").get_text(strip=True)
        availability = article.select_one(".availability").get_text(strip=True)

        rating_element = article.select_one(".star-rating")
        rating = rating_element["class"][1]

        book_url = urljoin(page_url, link["href"])

        book = {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": book_url,
        }

        books.append(book)

    return books


def get_next_page(html, page_url):
    soup = BeautifulSoup(html, "lxml")

    next_button = soup.select_one("li.next a")

    if next_button is None:
        return None

    return urljoin(page_url, next_button["href"])


def scrape_all_books(max_pages=None):
    books = []
    page_url = START_URL
    page_number = 0

    while page_url is not None:
        if max_pages is not None and page_number >= max_pages:
            break

        print(f"Scraping page {page_number + 1}: {page_url}")

        html = get_page(page_url)

        page_books = parse_books(html, page_url)
        books.extend(page_books)

        page_number += 1
        page_url = get_next_page(html, page_url)

    return books


def save_to_csv(books, filename):
    fieldnames = [
        "title",
        "price",
        "rating",
        "availability",
        "url",
    ]

    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)


def save_to_json(books, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            books,
            file,
            ensure_ascii=False,
            indent=4,
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Scrape books from books.toscrape.com"
    )

    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Output format (default: both)",
    )

    parser.add_argument(
        "--pages",
        type=int,
        default=None,
        help="Maximum number of pages to scrape",
    )

    args = parser.parse_args()

    if args.pages is not None and args.pages < 1:
        parser.error("--pages must be a positive integer")

    return args


def main():
    args = parse_arguments()

    try:
        books = scrape_all_books(args.pages)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if args.format in ("csv", "both"):
            csv_path = OUTPUT_DIR / "books.csv"
            save_to_csv(books, csv_path)
            print(f"Saved: {csv_path}")

        if args.format in ("json", "both"):
            json_path = OUTPUT_DIR / "books.json"
            save_to_json(books, json_path)
            print(f"Saved: {json_path}")

        print(f"\nTotal books scraped: {len(books)}")

    except (RuntimeError, OSError) as ex:
        print(f"Error: {ex}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()