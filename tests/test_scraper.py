from scraper import parse_books, get_next_page, save_to_csv, save_to_json, get_page
from unittest.mock import Mock, patch
import pytest
import csv
import json
import requests

def test_parse_books():
    html = """
    <html>
        <article class="product_pod">
            <h3>
                <a href="book_1.html" title="Python for Beginners">
                    Python for Beginners
                </a>
            </h3>

            <p class="price_color">£25.00</p>
            <p class="availability">In stock</p>
            <p class="star-rating Three"></p>
        </article>
    </html>
    """

    books = parse_books(
        html,
        "https://example.com/catalogue/page-1.html"
    )

    assert len(books) == 1
    assert books[0]["title"] == "Python for Beginners"
    assert books[0]["price"] == "£25.00"
    assert books[0]["rating"] == "Three"
    assert books[0]["availability"] == "In stock"
    assert books[0]["url"] == "https://example.com/catalogue/book_1.html"


def test_get_next_page():
    html = """
    <html>
        <li class="next">
            <a href="page-2.html">next</a>
        </li>
    </html>
    """

    next_page = get_next_page(
        html,
        "https://example.com/catalogue/page-1.html"
    )

    assert next_page == "https://example.com/catalogue/page-2.html"


def test_get_next_page_when_missing():
    html = "<html><body><p>No next page</p></body></html>"

    next_page = get_next_page(
        html,
        "https://example.com/catalogue/page-1.html"
    )

    assert next_page is None


def test_save_to_csv(tmp_path):
    books = [
        {
            "title": "Python Basics",
            "price": "£20.00",
            "rating": "Five",
            "availability": "In stock",
            "url": "https://example.com/book",
        }
    ]

    filename = tmp_path / "books.csv"
    save_to_csv(books, filename)

    with open(filename, encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0] == books[0]


def test_save_to_json(tmp_path):
    books = [
        {
            "title": "Python Basics",
            "price": "£20.00",
            "rating": "Five",
            "availability": "In stock",
            "url": "https://example.com/book",
        }
    ]

    filename = tmp_path / "books.json"
    save_to_json(books, filename)

    with open(filename, encoding="utf-8") as file:
        saved_books = json.load(file)

    assert saved_books == books


def test_get_page_success():
    fake_response = Mock()
    fake_response.text = "<html>Test page</html>"

    with patch("scraper.requests.get", return_value=fake_response) as mock_get:
        html = get_page("https://example.com")

    assert html == "<html>Test page</html>"

    mock_get.assert_called_once_with(
        "https://example.com",
        timeout=10,
    )


def test_get_page_failure():
    with patch(
        "scraper.requests.get",
        side_effect=requests.ConnectionError("Connection failed"),
    ) as mock_get:
        with patch("scraper.time.sleep"):
            with pytest.raises(RuntimeError):
                get_page("https://example.com")

    assert mock_get.call_count == 3