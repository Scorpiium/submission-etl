import pandas as pd

def save_to_csv(df, output_path='products.csv'):
    try:
        df.to_csv(output_path, index=False)
        print(f"Data berhasil disimpan ke {output_path}")
    except Exception as e:
        print(f"Gagal menyimpan data ke CSV: {e}")