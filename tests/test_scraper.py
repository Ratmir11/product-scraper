from scraper import parse_books, get_next_page


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