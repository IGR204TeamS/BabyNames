import polars as pl
import re
import os

data_dir_path = os.path.join('..', 'data')
data_file_path = os.path.join(data_dir_path, 'dpt2020.csv')
data_coord_path = os.path.join(data_dir_path, 'dpt.csv')

def load_baby_names_data(base_file_path=data_file_path, coord_file_path=data_coord_path):
    """
    Load data for the baby names project from CSV files using Polars.

    Parameters:
    base_file_path (str): The path to the CSV file for base data.
    coord_file_path (str): The path to the CSV file for coord data.

    Returns:
    DataFrame: A Polars DataFrame containing a merge of all the loaded data.
    """
    data = load_data(base_file_path)
    data_coord = load_coord_data(coord_file_path)
    baby_names_data = data.join(data_coord, on='dpt', how='left')
    return baby_names_data

def load_data(file_path):
    """
    Load data from a CSV file using Polars.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A Polars DataFrame containing the loaded data.
    """

    # Define the data types
    dtypes = {
        'sexe': pl.Int64,
        'preusuel': pl.Utf8,
        'annais': pl.Utf8,
        'dpt': pl.Utf8,
        'nombre': pl.Int64
    }

    # Load the data
    data = pl.read_csv(file_path, dtypes=dtypes)

    return data

def load_coord_data(file_path):
    """
    Load data from a CSV file using Polars.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A Polars DataFrame containing the loaded data.
    """
    # Load the data
    data = pl.read_csv(file_path)

    # Apply the conversion function to the 'longitude' and 'latitude' columns
    data = data.with_columns(data['longitude'].apply(dms_to_dd).alias('longitude'))
    data = data.with_columns(data['latitude'].apply(dms_to_dd).alias('latitude'))

    return data

def dms_to_dd(dms):
    """
    Convert degrees, minutes, and seconds to decimal degrees.

    Parameters:
    dms (str): A string representing degrees, minutes, and seconds in the format 'D°M'S" O/E'.

    Returns:
    float: The equivalent value in decimal degrees.
    """
    degrees, minutes, seconds, direction = re.split('[°\'"]+', dms)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction in ('S','O'):
        dd *= -1
    return dd