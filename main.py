from utils.extract import scrape_all_products
from utils.transform import transform_data
from utils.load import save_to_csv

def main():
    url = 'https://fashion-studio.dicoding.dev/'

    extracted_data = scrape_all_products(url)

    if extracted_data.empty:
        print("Tidak ada data yang berhasil diambil.")
        return

    print("Transformasi data...")
    df_transformed_data = transform_data(extracted_data)
    print(df_transformed_data)

    print("Menyimpan data ke CSV...")
    save_to_csv(df_transformed_data)

if __name__ == "__main__":
    main()