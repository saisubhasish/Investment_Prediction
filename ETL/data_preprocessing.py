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

class Preprocess:
    @staticmethod
    def data_wrangling(br, itc, rel, tcs, tatam):
        logging.info("Reading the raw data from directory")
        df_rel = pd.read_csv(rel)
        df_br = pd.read_csv(br)
        df_itc = pd.read_csv(itc)
        df_tcs = pd.read_csv(tcs)
        df_tatam = pd.read_csv(tatam)

        logging.info("Preparing list of dataframes")
        df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]

        logging.info("Defining stock name list")
        symbol_list = ['BRITANNIA', 'ITC', 'RELIANCE', 'TATAMOTORS', 'TCS']

        logging.info("Adding 'Symbol' column to dataframe")
        try:
            utils.add_symbol(df_list, symbol_list)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        logging.info("Pre-processing the raw data")

        try:
            logging.info("Dropping 'Unnamed : 0' column from dataframes")
            list(map(utils.column_drop, df_list))
            
            logging.info('Converting "Volume" column values to numerical')
            list(map(utils.convert_value_to_numerical, df_list))

            logging.info("Converting 'Chg%' column the values to numerical")
            list(map(utils.convert_percentage_value, df_list))

            logging.info("Converting datatype of 'Date' column")
            logging.info("Removing the extra characters from Date column")
            list(map(utils.date_operarion, df_list))

            logging.info("Setting 'Date' as index")
            list(map(utils.set_index_as_Date, df_list))

        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        print(df_itc)
            
        logging.info(f"Saving the processed data to : {file_path}")

        df_br.to_csv(f'{file_path}britannia-industries.csv')
        df_itc.to_csv(f'{file_path}itc.csv')
        df_rel.to_csv(f'{file_path}reliance-industries.csv')
        df_tcs.to_csv(f'{file_path}tata-consultancy-services.csv')
        df_tatam.to_csv(f'{file_path}tata-motors-ltd.csv')

Preprocess.data_wrangling(br, itc, rel, tcs, tatam)