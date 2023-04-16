import os
import sys
import json
import pymongo
import pandas as pd
from investment_prediction.config import mongo_client
from investment_prediction.logger import logging
from investment_prediction.exception import InvestmentPredictionException


class Data_Loading:
    @staticmethod
    def dump(preprocessed_file_path, DATABASE_NAME, company_list):
        logging.info(f"{'>>'*20} Data Dump {'<<'*20}")
        logging.info('Getting the list of file names from pre-processed directory')
        file_list = os.listdir(preprocessed_file_path)

        logging.info(f'File list: {file_list}')

        DATA_FILE_PATH_br = f"{os.getcwd()}\\pre_processed_dataset\\{file_list[0]}"
        DATA_FILE_PATH_itc = f"{os.getcwd()}\\pre_processed_dataset\\{file_list[1]}"
        DATA_FILE_PATH_rel = f"{os.getcwd()}\\pre_processed_dataset\\{file_list[2]}"
        DATA_FILE_PATH_tcs = f"{os.getcwd()}\\pre_processed_dataset\\{file_list[3]}"
        DATA_FILE_PATH_tatam = f"{os.getcwd()}\\pre_processed_dataset\\{file_list[4]}"

        logging.info('Reading pre-processed data to store in database')
        df_br = pd.read_csv(DATA_FILE_PATH_br)
        df_itc = pd.read_csv(DATA_FILE_PATH_itc)
        df_rel = pd.read_csv(DATA_FILE_PATH_rel)
        df_tatam = pd.read_csv(DATA_FILE_PATH_tatam)
        df_tcs = pd.read_csv(DATA_FILE_PATH_tcs)
        print(f"""Rows and columns of df_br: {df_br.shape}\nRows and columns of df_itc: {df_itc.shape}\nRows and columns
            of df_rel: {df_rel.shape}\nRows and columns of df_tatam: {df_tatam.shape}\nRows and columns of df_tcs: {df_tcs.shape}""")
        
        logging.info("Preparing list of dataframes")
        df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]
        
        try:
            logging.info('Updating records to insert data to mongoDB')
            logging.info("Resetting index")
            list(map(lambda df: df.reset_index(drop=True,inplace=True), df_list))

            logging.info("Converting the 'Date' column datatype")
            for df in df_list:
                df['Date'] = pd.to_datetime(df['Date'])

            logging.info("Convert dataframe to json type(dict) so that we can dump these record in mongo db")
            logging.info("Each record will represent one row")
            json_record_br = df_br.to_dict('records')
            print(json_record_br)
            json_record_itc = df_itc.to_dict('records')
            print(json_record_itc)
            json_record_rel = df_rel.to_dict('records')
            print(json_record_rel)
            json_record_tatam = df_tatam.to_dict('records')
            print(json_record_tatam)
            json_record_tcs = df_tcs.to_dict('records')
            print(json_record_tcs)

        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        logging.info("Preparing list of json records")
        json_record_list = [json_record_br, json_record_itc, json_record_rel, json_record_tatam, json_record_tcs]

        print(json_record_list[1])
        
        logging.info("inserting converted json record to mongo db")
        try:
            logging.info("Creating collection using company list")
            list(map(lambda company : mongo_client[DATABASE_NAME].create_collection(company, timeseries= {"timeField": "Date", "metaField": "metadata", "granularity": "seconds"}), company_list))
            
            logging.info("Preparing list of collections")
            collection_list = mongo_client[DATABASE_NAME].list_collection_names()

            i = 0
            for collection in collection_list:
                if collection == 'britannia-industries':
                    mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[0])
                    print(f'Record inserted successfully in collection: {collection}')
                elif collection == 'itc':
                    mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[1])
                    print(f'Record inserted successfully in collection: {collection}')
                elif collection == 'reliance-industries':
                    mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[2])
                    print(f'Record inserted successfully in collection: {collection}')
                elif collection == 'tata-motors-ltd':
                    mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[3])
                    print(f'Record inserted successfully in collection: {collection}')
                elif collection == 'tata-consultancy-services':
                    mongo_client[DATABASE_NAME][collection].insert_many(json_record_list[4])
                    print(f'Record inserted successfully in collection: {collection}')
                    
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

 