import polars as pl

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
