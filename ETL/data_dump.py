import json
import pymongo
import pandas as pd
from investment_prediction.config import mongo_client
from investment_prediction.logger import logging


DATA_FILE_PATH_br = 'D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/britannia-industries.csv'
DATA_FILE_PATH_itc = 'D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/itc.csv'
DATA_FILE_PATH_rel = 'D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/reliance-industries.csv'
DATA_FILE_PATH_tatam = 'D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/tata-motors-ltd.csv'
DATA_FILE_PATH_tcs = 'D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/pre_processed_dataset/tata-consultancy-services.csv'

DATABASE_NAME="TimeSeries"

COLLECTION_NAME_br="BRITANNIA"
COLLECTION_NAME_itc = 'ITC'
COLLECTION_NAME_rel = 'RELIANCE'
COLLECTION_NAME_tatam = 'TATAMOTORS'
COLLECTION_NAME_tcs = 'TCS'


class Data_Loading:
    @staticmethod
    def dump(DATABASE_NAME):
        df_br = pd.read_csv(DATA_FILE_PATH_br)
        df_itc = pd.read_csv(DATA_FILE_PATH_itc)
        df_rel = pd.read_csv(DATA_FILE_PATH_rel)
        df_tatam = pd.read_csv(DATA_FILE_PATH_tatam)
        df_tcs = pd.read_csv(DATA_FILE_PATH_tcs)
        print(f"""Rows and columns of df_br: {df_br.shape}\nRows and columns of df_itc: {df_itc.shape}\nRows and columns
            of df_rel: {df_rel.shape}\nRows and columns of df_tatam: {df_tatam.shape}\nRows and columns of df_tcs: {df_tcs.shape}""")
        
        logging.info("Preparing list of dataframes")
        df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]

        logging.info("Preparing list of collections")
        collection_list = [COLLECTION_NAME_br, COLLECTION_NAME_itc, COLLECTION_NAME_rel, COLLECTION_NAME_tatam, COLLECTION_NAME_tcs]

        logging.info("Resetting index")
        for df in df_list:
            df.reset_index(drop=True,inplace=True)

        logging.info("Converting the 'Date' column datatype")
        for df in df_list:
            df['Date'] = pd.to_datetime(df['Date'])

        logging.info("Convert dataframe to json so that we can dump these record in mongo db")
        logging.info("Each record will represent one row")
        json_record_br = df_br.to_dict('records')
        json_record_itc = df_itc.to_dict('records')
        json_record_rel = df_rel.to_dict('records')
        json_record_tatam = df_tatam.to_dict('records')
        json_record_tcs = df_tcs.to_dict('records')

        logging.info("Preparing list of json records")
        json_record_list = [json_record_br, json_record_itc, json_record_rel, json_record_tatam, json_record_tcs]

        print(json_record_br[1])

        logging.info("inserting converted json record to mongo db")
        i = 0
        for collection in collection_list:
            mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[i])
            i+=1

    # Function call
Data_Loading.dump(DATABASE_NAME)