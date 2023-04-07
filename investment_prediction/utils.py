import os
import sys
import pandas as pd
import numpy as np
from investment_prediction.config import mongo_client
from investment_prediction.logger import logging
from investment_prediction.exception import InvestmentPredictionException


def add_symbol(df_list, symbol_list):
    """
    Description: This function adds column 'Symbol' in dataframes
    =========================================================
    Params:
    df_list: List of dataframes
    symbol_list: List of Stock symbols
    =========================================================
    """
    i = 0
    for df in df_list:
        df['Symbol'] = symbol_list[i]
        i+=1

def column_drop(df):
    """
    Description: This function drops the 'Unnamed: 0' column from dataframe
    =========================================================
    Params:
    df : data frame
    =========================================================
    return Pandas dataframe
    """
    try:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    except Exception as e:
        raise InvestmentPredictionException(e, sys)

    return df

def convert_to_int(value):
    """
    _summary_ : This function replaces M with 100000 and K with 1000
    Args:
        value (alphanumeric): _description_
    Returns:
        numeric: replaced
    """
    try:
        if value.endswith('M'):
            return int(float(value[:-1]) * 1000000)
        elif value.endswith('K'):
            return int(float(value[:-1]) * 1000)
        else:
            return int(value)
    
    except Exception as e:
        raise InvestmentPredictionException(e, sys)
    
def convert_value_to_numerical(df):
    """
    Description: This function converts the value of "volume" column 
    =========================================================
    Params:
    df : data frame
    =========================================================
    returs Pandas dataframe
    """
    try:
        values = df['Volume']
        df['Volume'] = df['Volume'].apply(convert_to_int)

    except Exception as e:
        raise InvestmentPredictionException(e, sys)

    return df

def convert_percentage_to_float(value):
    """
    _summary_ : This function replaces % with 0.001
    Args:
        value (number and special character): _description_
    Returns:
        numeric: replaced
    """
    return float(value.replace('%', ''))/100

def convert_percentage_value(df):
    """
    Description: This function will convert 'Chg%' column values to numeric
    =========================================================
    Params:
    df : data frame
    =========================================================
    return Pandas dataframe
    """
    try:
        df['Chg%'] = df['Chg%'].apply(convert_percentage_to_float)
    except Exception as e:
        raise InvestmentPredictionException(e, sys)
    
    return df

def date_operarion(df):
    """
    Description: This function removes anomalies from 'Date' column
    =========================================================
    Params:
    dataframe: df
    =========================================================
    return Pandas dataframe
    """
    try:
        df['Date'] = df['Date'].map(lambda x: str(x).strip().rstrip('E').rstrip('D').rstrip('S').rstrip(' S '))
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        raise InvestmentPredictionException(e, sys)
    
    return df

def set_index_as_Date(df):
    """
    Description: This function sets the 'Date' column as index
    =========================================================
    Params:
    dataframe: df
    =========================================================
    return Pandas dataframe
    """
    try:
        df.set_index('Date', inplace=True)
    except Exception as e:
        raise InvestmentPredictionException(e, sys)

    return df

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:    
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    
    except Exception as e:
        raise InvestmentPredictionException(e, sys)

def split_data(df, test_size):
    """
    Description: This function returns numpy array data
    =========================================================
    Params:
    df: data frame
    test_size: split size
    =========================================================
    returns train_set nad test_set
    """
    try:
        X = df.values # Convert to NumPy array
        split = int(len(X) * (1-test_size))
        train_set = X[: split]
        test_set = X[split:]
        return train_set, test_set
    
    except Exception as e:
        raise InvestmentPredictionException(e, sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise InvestmentPredictionException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise InvestmentPredictionException(e, sys) from e