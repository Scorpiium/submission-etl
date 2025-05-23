import os
import pandas as pd
from utils.load import save_to_csv
from unittest.mock import patch

def test_save_to_csv_success(tmp_path):
    # DataFrame dummy
    df = pd.DataFrame({
        'Title': ['Item A'],
        'Price': [100.0],
        'Rating': [4.5],
        'Colors': [3],
        'Size': ['L'],
        'Gender': ['Male'],
        'Timestamp': ['2025-05-18T12:00:00']
    })

    output_path = tmp_path / "test_output.csv"
    save_to_csv(df, output_path=str(output_path))

    # Verifikasi file CSV berhasil disimpan
    assert output_path.exists()
    loaded_df = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(loaded_df, df)


def test_save_to_csv_failure(capfd):
    df = pd.DataFrame({'A': [1, 2]})

    # Patch to_csv agar menimbulkan exception
    with patch('pandas.DataFrame.to_csv', side_effect=Exception("Disk write error")):
        save_to_csv(df, output_path="fake_output.csv")

    captured = capfd.readouterr()
    assert "Gagal menyimpan data ke CSV" in captured.out