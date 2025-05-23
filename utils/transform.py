import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah list of dict menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate=16000):
    """Melakukan transformasi data produk: konversi harga, parsing rating, filter data tidak valid."""
    try:
        # Filter data tidak valid
        data = data[data['Title'] != 'Unknown Product']
        data = data[~data['Rating'].str.contains('Invalid Rating', na=False)]
        data = data[~data['Price'].str.contains('Price Unavailable', na=False)]
        data = data[~data['Price'].isin(['N/A', None])]
        data = data[~data['Rating'].isin(['N/A', None])]

        # Konversi Rating: '4.3 out of 5' → 4.3
        data['Rating'] = data['Rating'].str.extract(r'(\d\.\d)').astype(float)

        # Konversi Price: '$9.99' → 9.99, lalu ke rupiah
        data['Price_in_usd'] = data['Price'].replace(r'[\$,]', '', regex=True).astype(float)
        data['Price_in_rupiah'] = (data['Price_in_usd'] * exchange_rate)

        # Konversi Colors: '3 colors' → 3
        data['Colors'] = data['Colors'].str.extract(r'(\d+)').astype(int)

        # Bersihkan Size & Gender
        data['Size'] = data['Size'].str.replace('Size: ', '', regex=False)
        data['Gender'] = data['Gender'].str.replace('Gender: ', '', regex=False)

        # Drop kolom yang tidak dibutuhkan
        data = data.drop(columns=['Price', 'Price_in_usd'])

        # Set tipe data
        data['Title'] = data['Title'].astype('string')
        data['Size'] = data['Size'].astype('string')
        data['Gender'] = data['Gender'].astype('string')

        return data

    except Exception as e:
        print(f"Gagal mentransformasi data: {e}")
        return pd.DataFrame()