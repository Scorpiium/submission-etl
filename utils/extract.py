import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Gagal mengambil konten dari {url}: {e}")
        return None

def extract_product_data(card, timestamp):
    try:
        product_details = card.find('div', class_='product-details')
        title_tag = product_details.find('h3', class_='product-title')
        title = title_tag.text.strip() if title_tag else 'N/A'

        price_tag = product_details.find('div', class_='price-container')
        price = price_tag.find('span', class_='price').text.strip() if price_tag else 'N/A'

        paragraphs = product_details.find_all('p')
        rating = paragraphs[0].text.strip() if len(paragraphs) > 0 else 'N/A'
        color = paragraphs[1].text.strip() if len(paragraphs) > 1 else 'N/A'
        size = paragraphs[2].text.strip() if len(paragraphs) > 2 else 'N/A'
        gender = paragraphs[3].text.strip() if len(paragraphs) > 3 else 'N/A'

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": color,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }
    except Exception as e:
        print(f"Gagal mengekstrak data produk: {e}")
        return {
            "Title": "N/A",
            "Price": "N/A",
            "Rating": "N/A",
            "Colors": "N/A",
            "Size": "N/A",
            "Gender": "N/A",
            "Timestamp": timestamp
        }

def scrape_all_products(base_url, delay=2):
    data = []
    page_number = 1

    while True:
        url = base_url if page_number == 1 else f"{base_url}page{page_number}"
        print(f"Mengakses halaman: {url}")
        html_content = fetch_page_content(url)
        if not html_content:
            print("Konten halaman tidak dapat diambil, proses dihentikan.")
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        main = soup.find('main', class_='container')
        if not main:
            print("Elemen utama <main> tidak ditemukan pada halaman.")
            break

        grid = main.find('div', class_='collection-grid')
        if not grid:
            print("Tidak ada produk ditemukan di grid koleksi.")
            break

        cards = grid.find_all('div', class_='collection-card')
        if not cards:
            print("Tidak ada produk tersedia di halaman ini.")
            break

        for card in cards:
            timestamp = datetime.now().isoformat()
            product = extract_product_data(card, timestamp)
            data.append(product)

        pagination_container = main.find('div', class_='container')
        next_button = pagination_container.find('li', class_='page-item next') if pagination_container else None
        if next_button:
            page_number += 1
            time.sleep(delay)
        else:
            print("Halaman terakhir telah dicapai.")
            break

    return pd.DataFrame(data)