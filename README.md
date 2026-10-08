# 📚 Python Book Scraper

A command-line Python scraper that collects book information from [Books to Scrape](https://books.toscrape.com/) and exports it as CSV, JSON, or both.

## Features

- Extracts book title, price, star rating, availability, and product URL.
- Follows pagination automatically (up to 50 pages / 1,000 books on the practice site).
- Exports data to CSV and JSON in the `output/` directory.
- Supports limiting the number of pages and choosing the output format.
- Retries failed HTTP requests up to three times, with a delay between attempts.

## Tech stack

- Python 3
- Requests
- BeautifulSoup4 with lxml
- Python standard library: `argparse`, `csv`, `json`, `pathlib`

## Getting started

Clone the repository:

```bash
git clone git@github.com:Ratmir11/product-scraper.git
cd product-scraper
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows (PowerShell), activate it with `venv\Scripts\Activate.ps1` instead.

Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure `lxml` is included in `requirements.txt` because the scraper uses `BeautifulSoup(html, "lxml")`.

## Usage

```bash
# Scrape all available pages and save both formats
python scraper.py

# Export only CSV
python scraper.py --format csv

# Export only JSON
python scraper.py --format json

# Scrape the first 5 pages, saving both formats
python scraper.py --pages 5 --format both

# Show command-line options
python scraper.py --help
```

Generated files are written to:

```text
output/
├── books.csv
└── books.json
```

Only the requested output format is updated; previously generated files in the other format are not automatically deleted.

## Data fields

| Field | Description |
| --- | --- |
| `title` | Book title |
| `price` | Price as shown on the site |
| `rating` | Star rating label (e.g. `Three`) |
| `availability` | Availability text |
| `url` | Absolute link to the book page |

Example JSON record:

```json
{
  "title": "A Light in the Attic",
  "price": "£51.77",
  "rating": "Three",
  "availability": "In stock",
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

## Error handling

HTTP requests use a 10-second timeout and are retried up to three times with a two-second delay between attempts. If the page cannot be fetched, the script exits with an error rather than attempting to parse missing HTML. Retry behavior is currently basic: all `requests` errors are retried, including HTTP errors that may not be transient.

## Project structure

```text
product-scraper/
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
└── output/             # Created when the scraper runs
    ├── books.csv
    └── books.json
```

Some versions of the repository may also contain sample `books.csv` and `books.json` files in the project root.

## Notes

[Books to Scrape](https://books.toscrape.com/) is a demonstration website intended for practicing web scraping. This project is for learning and portfolio purposes.

## Author

[**Ratmir11**](https://github.com/Ratmir11)
