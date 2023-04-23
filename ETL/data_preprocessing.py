import os
import sys
import pandas as pd
import numpy as np
from investment_prediction import utils
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging



class Data_Wrangling:
    @staticmethod
    def data_cleaning(raw_file_path, preprocessed_file_path):

        logging.info(f"{'>>'*20} Data Preprocessing {'<<'*20}")

        logging.info('Getting the list of file names from raw directory')
        file_list = os.listdir(raw_file_path)

        logging.info(f'File list: {file_list}')

        logging.info('Getting the path to read each raw file')
        br = f"{os.getcwd()}\\raw_dataset\\{file_list[0]}"
        itc = f"{os.getcwd()}\\raw_dataset\\{file_list[1]}"
        rel = f"{os.getcwd()}\\raw_dataset\\{file_list[2]}"
        tcs = f"{os.getcwd()}\\raw_dataset\\{file_list[3]}"
        tatam = f"{os.getcwd()}\\raw_dataset\\{file_list[4]}"

        logging.info("Reading the raw data from directory")
        df_br = pd.read_csv(br)
        df_rel = pd.read_csv(rel)
        df_itc = pd.read_csv(itc)
        df_tatam = pd.read_csv(tatam)
        df_tcs = pd.read_csv(tcs)

        logging.info("Preparing list of dataframes")
        df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]

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

            logging.info("Creating pre-processed file path if not exists")
            if not os.path.exists(preprocessed_file_path):
                os.makedirs(preprocessed_file_path)

        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
        try:
            logging.info("Reversing the data in dataframe")
            df_br = df_br[::-1]
            df_itc = df_itc[::-1]
            df_rel = df_rel[::-1]
            df_tcs = df_tcs[::-1]
            df_tatam = df_tatam[::-1]

        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        print(df_br)
        print(df_itc)
        print(df_rel)
        print(df_tcs)
        print(df_tatam)
            
        logging.info(f"Saving the processed data to : {preprocessed_file_path}")

        df_br.to_csv(preprocessed_file_path+'/britannia-industries.csv')
        df_itc.to_csv(preprocessed_file_path+'/itc.csv')
        df_rel.to_csv(preprocessed_file_path+'/reliance-industries.csv')
        df_tcs.to_csv(preprocessed_file_path+'/tata-consultancy-services.csv')
        df_tatam.to_csv(preprocessed_file_path+'/tata-motors-ltd.csv')


