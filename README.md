# 📚 Python Book Scraper

A command-line Python web scraper that collects book information from [Books to Scrape](https://books.toscrape.com/) and exports the results to CSV, JSON, or both.

Built as a portfolio project to demonstrate web scraping, pagination, data extraction, error handling, and automated testing in Python.

## Features

- Extracts book titles, prices, star ratings, availability, and product URLs.
- Follows pagination automatically (the practice site contains up to 50 pages and 1,000 books).
- Exports results to CSV, JSON, or both in the `output/` directory.
- Supports limiting the number of pages through command-line arguments.
- Uses a 10-second request timeout and retries failed requests up to three times.
- Skips book cards that are missing required elements such as title, price, rating, or availability.
- Includes automated tests for parsing, pagination, exports, and error handling.

## Tech Stack

- Python 3
- Requests
- Beautiful Soup 4
- lxml
- pytest
- Python standard library: `argparse`, `csv`, `json`, `pathlib`

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Ratmir11/product-scraper.git
cd product-scraper
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows (PowerShell), activate the environment with:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The scraper uses the `lxml` parser, so `lxml` must be installed alongside Beautiful Soup.

## Usage

Run the scraper from the project root:

```bash
# Scrape all available pages and save both formats
python scraper.py

# Export only CSV
python scraper.py --format csv

# Export only JSON
python scraper.py --format json

# Scrape the first 5 pages and save both formats
python scraper.py --pages 5 --format both

# Show available command-line options
python scraper.py --help
```

Generated files are saved in the `output/` directory:

```text
output/
├── books.csv
└── books.json
```

Only the requested output format is updated. Previously generated files in another format are not automatically deleted.

## Data Fields

| Field | Description |
| --- | --- |
| `title` | Book title |
| `price` | Price as displayed on the website |
| `rating` | Star rating label, such as `Three` |
| `availability` | Availability text |
| `url` | Absolute URL of the book's product page |

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

## Testing

The project includes automated tests written with `pytest`.

Run the full test suite from the project root:

```bash
python -m pytest -v
```

The tests cover:

- Extracting book information from HTML.
- Finding the next page and handling the end of pagination.
- Saving and reading CSV and JSON output.
- Successful and failed HTTP requests, including retry behavior.
- Scraping multiple pages with mocked responses.
- Skipping incomplete book cards when required fields are missing.

Mocks and `monkeypatch` keep the tests independent of the live website.

## Error Handling

HTTP requests use a 10-second timeout and are retried up to three times with a delay between attempts. If a page cannot be fetched after the retries, the scraper raises an error rather than trying to parse missing HTML.

Book cards missing required elements are skipped so that a single incomplete card does not interrupt parsing the rest of the page.

**Current limitations:** The retry strategy also retries HTTP errors that may not be temporary. A rating element with unexpected CSS classes may still require additional validation.

## Project Structure

```text
product-scraper/
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
├── tests/
│   └── test_scraper.py
└── output/             # Created when the scraper runs
    ├── books.csv
    └── books.json
```

Some versions of the repository may also contain sample `books.csv` and `books.json` files in the project root.

## Notes

[Books to Scrape](https://books.toscrape.com/) is a demonstration website intended for web scraping practice. This project is intended for learning and portfolio purposes.

## Author

[**Ratmir11**](https://github.com/Ratmir11)
