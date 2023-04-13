from investment_prediction import utils
from investment_prediction.entity import config_entity, artifact_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from investment_prediction.utils import split_data
import os,sys
import pandas as pd 
import numpy as np

class DataIngestion:
    
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig ):
        '''
        Storing the input to a variable to use in pipeline
        '''
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        """
        This function takes Input: Database name and collection name
        and returns output: feature store file, train file and test file
        """
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df_br:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)
            print(df_br)

            df_itc:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_itc)
            print(df_itc)

            df_rel:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_rel)
            print(df_rel)

            df_tatam:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_tatam)
            print(df_tatam)
            
            df_tcs:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_tcs)
            print(df_tcs)
            

            logging.info("Save data in feature store")
            logging.info("Create Dataset store folder if not available")
            feature_store_dir_br = os.path.dirname(self.data_ingestion_config.dataset1_file_path)
            os.makedirs(feature_store_dir_br,exist_ok=True)
            feature_store_dir_itc = os.path.dirname(self.data_ingestion_config.dataset2_file_path)
            os.makedirs(feature_store_dir_itc,exist_ok=True)
            feature_store_dir_rel = os.path.dirname(self.data_ingestion_config.dataset3_file_path)
            os.makedirs(feature_store_dir_rel,exist_ok=True)
            feature_store_dir_tatam = os.path.dirname(self.data_ingestion_config.dataset4_file_path)
            os.makedirs(feature_store_dir_tatam,exist_ok=True)
            feature_store_dir_tcs = os.path.dirname(self.data_ingestion_config.dataset5_file_path)
            os.makedirs(feature_store_dir_tcs,exist_ok=True)

            logging.info("Save df to feature store folder ==>> Dataset")
            df_br.to_csv(path_or_buf=self.data_ingestion_config.dataset1_file_path, index=False, header=True)
            df_itc.to_csv(path_or_buf=self.data_ingestion_config.dataset2_file_path, index=False, header=True)
            df_rel.to_csv(path_or_buf=self.data_ingestion_config.dataset3_file_path, index=False, header=True)
            df_tatam.to_csv(path_or_buf=self.data_ingestion_config.dataset4_file_path, index=False, header=True)
            df_tcs.to_csv(path_or_buf=self.data_ingestion_config.dataset5_file_path, index=False, header=True)
            
            logging.info("Preparing data ingestion artifacts") 
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                dataset1_file_path=self.data_ingestion_config.dataset1_file_path,
                dataset2_file_path=self.data_ingestion_config.dataset2_file_path,
                dataset3_file_path=self.data_ingestion_config.dataset3_file_path,
                dataset4_file_path=self.data_ingestion_config.dataset4_file_path,
                dataset5_file_path=self.data_ingestion_config.dataset5_file_path)
                #train_file_path=self.data_ingestion_config.train_file_path_br, 
                #test_file_path=self.data_ingestion_config.test_file_path_br

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise InvestmentPredictionException(error_message=e, error_detail=sys)



        
