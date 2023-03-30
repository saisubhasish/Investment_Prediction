import pandas as pd
from investment_prediction.logger import logging


def column_drop(df):
    """
    Description: This function drops the 'Unnamed: 0' column from dataframe
    =========================================================
    Params:
    dataframe: df
    =========================================================
    return Pandas dataframe
    """
    logging.info("Function to drop 'Unnamed' column")
    df.drop('Unnamed: 0', axis=1, inplace=True)
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
    logging.info('Converting "Volume" column values to numerical')
    values = df['Volume']
    df['Volume'] = df['Volume'].apply(convert_to_int)
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
    logging.info("Converting 'Chg%' column the values to numerical")
    df['Chg%'] = df['Chg%'].apply(convert_percentage_to_float)
    return df

def date_operarion(df):
    logging.info("Converting datatype of 'Date' column")
    logging.info("Removing the extra characters from Date column")
    df['Date'] = df['Date'].map(lambda x: str(x).strip().rstrip('E').rstrip('D').rstrip('S').rstrip(' S '))
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def set_index_as_Date(df):
    logging.info("Setting 'Date' as index")
    df.set_index('Date', inplace=True)
    return df
