import pytest
import requests
import pandas as pd
from unittest.mock import patch, Mock
from utils.extract import fetch_page_content, extract_product_data, scrape_all_products
from datetime import datetime

# HTML dummy untuk simulasi struktur produk
MOCK_HTML = '''
<main class="container">
    <div class="collection-grid">
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Test Product</h3>
                <div class="price-container"><span class="price">$9.99</span></div>
                <p>4.3 out of 5</p>
                <p>3 colors</p>
                <p>Size: L</p>
                <p>Gender: Male</p>
            </div>
        </div>
    </div>
    <div class="container"></div>
</main>
'''

# HTML dummy tanpa produk
MOCK_EMPTY_HTML = '''
<main class="container">
    <div class="collection-grid">
    </div>
</main>
'''

def test_fetch_page_content_success():
    with patch('utils.extract.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html></html>'
        mock_get.return_value = mock_response

        content = fetch_page_content("http://example.com")
        assert content == b'<html></html>'

def test_fetch_page_content_failure():
    with patch('utils.extract.requests.get', side_effect=requests.RequestException("Connection error")):
        content = fetch_page_content("http://invalid-url.com")
        assert content is None

def test_extract_product_data_success():
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(MOCK_HTML, 'html.parser')
    card = soup.find('div', class_='collection-card')
    timestamp = datetime.now().isoformat()

    result = extract_product_data(card, timestamp)

    assert result['Title'] == 'Test Product'
    assert result['Price'] == '$9.99'
    assert result['Rating'] == '4.3 out of 5'
    assert result['Colors'] == '3 colors'
    assert result['Size'] == 'Size: L'
    assert result['Gender'] == 'Gender: Male'
    assert result['Timestamp'] == timestamp

def test_extract_product_data_missing_fields():
    from bs4 import BeautifulSoup
    html = '<div class="collection-card"><div class="product-details"></div></div>'
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div', class_='collection-card')
    timestamp = datetime.now().isoformat()

    result = extract_product_data(card, timestamp)
    assert result['Title'] == 'N/A'
    assert result['Price'] == 'N/A'
    assert result['Rating'] == 'N/A'
    assert result['Colors'] == 'N/A'
    assert result['Size'] == 'N/A'
    assert result['Gender'] == 'N/A'
    assert result['Timestamp'] == timestamp

def test_scrape_all_products_single_page():
    with patch('utils.extract.fetch_page_content', return_value=MOCK_HTML):
        df = scrape_all_products("http://fake-url.com/")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert df.iloc[0]["Title"] == "Test Product"

def test_scrape_all_products_empty_page():
    with patch('utils.extract.fetch_page_content', return_value=MOCK_EMPTY_HTML):
        df = scrape_all_products("http://fake-url.com/")
        assert isinstance(df, pd.DataFrame)
        assert df.empty