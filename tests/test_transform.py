import pandas as pd
import pytest
from utils.transform import transform_to_DataFrame, transform_data

def test_transform_to_dataframe():
    # Uji konversi list of dict ke DataFrame
    data = [
        {
            'Title': 'Product A',
            'Rating': '4.5 out of 5',
            'Price': '$10.00',
            'Colors': '5 colors',
            'Size': 'Size: M',
            'Gender': 'Gender: Unisex',
            'Timestamp': '2025-05-18T12:00:00'
        }
    ]
    df = transform_to_DataFrame(data)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Title' in df.columns

def test_transform_data_valid():
    # DataFrame dengan data valid
    data = {
        'Title': ['Product A'],
        'Rating': ['4.5 out of 5'],
        'Price': ['$10.00'],
        'Colors': ['5 colors'],
        'Size': ['Size: M'],
        'Gender': ['Gender: Unisex'],
        'Timestamp': ['2025-05-18T12:00:00']
    }
    df = pd.DataFrame(data)
    transformed_df = transform_data(df, exchange_rate=16000)

    assert not transformed_df.empty
    assert transformed_df.loc[0, 'Rating'] == 4.5
    assert transformed_df.loc[0, 'Price_in_rupiah'] == 160000.0
    assert transformed_df.loc[0, 'Colors'] == 5
    assert transformed_df.loc[0, 'Size'] == 'M'
    assert transformed_df.loc[0, 'Gender'] == 'Unisex'
    assert 'Price' not in transformed_df.columns
    assert 'Price_in_usd' not in transformed_df.columns

def test_transform_data_invalid():
    # Data dengan berbagai kondisi tidak valid
    data = {
        'Title': ['Unknown Product'],
        'Rating': ['Invalid Rating'],
        'Price': ['Price Unavailable'],
        'Colors': ['no colors'],
        'Size': ['Size: L'],
        'Gender': ['Gender: Male'],
        'Timestamp': ['2025-05-18T12:00:00']
    }
    df = pd.DataFrame(data)
    transformed_df = transform_data(df)

    # Seharusnya dikembalikan sebagai DataFrame kosong
    assert transformed_df.empty