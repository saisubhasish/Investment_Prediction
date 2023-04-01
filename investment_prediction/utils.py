import sys
import pandas as pd
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
    dataframe: df
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
    if value.endswith('M'):
        return int(float(value[:-1]) * 1000000)
    elif value.endswith('K'):
        return int(float(value[:-1]) * 1000)
    else:
        return int(value)
    
def convert_value_to_numerical(df):
    """
    Description: This function converts the value of "volume" column 
    =========================================================
    Params:
    dataframe: df
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
    dataframe: df
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
