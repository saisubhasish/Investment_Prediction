import sys
import pandas as pd
import numpy as np
from investment_prediction import utils
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging

file_path = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/"

br = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/britannia-industries.csv"
itc = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/itc.csv"
rel = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/reliance-industries.csv"
tcs = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/tata-consultancy-services.csv"
tatam = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/tata-motors-ltd.csv"

logging.info("Reading the raw data from directory")
df_rel = pd.read_csv(rel)
df_br = pd.read_csv(br)
df_itc = pd.read_csv(itc)
df_tcs = pd.read_csv(tcs)
df_tatam = pd.read_csv(tatam)

logging.info("Preparing list of dataframes")
df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]

for df in df_list:
    try:
        utils.column_drop(df)
        utils.convert_value_to_numerical(df)
        utils.convert_percentage_value(df)
        utils.date_operarion(df)
        utils.set_index_as_Date(df)

    except Exception as e:
        raise InvestmentPredictionException(e, sys)

df_br.to_csv(f'{file_path}britannia-industries.csv')
df_itc.to_csv(f'{file_path}itc.csv')
df_rel.to_csv(f'{file_path}reliance-industries.csv')
df_tcs.to_csv(f'{file_path}tata-consultancy-services.csv')
df_tatam.to_csv(f'{file_path}tata-motors-ltd.csv')