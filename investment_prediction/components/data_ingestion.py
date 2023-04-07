
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
            # Exporting collection data as pandas dataframe
            df_br:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_br)
            df_itc:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_itc)
            df_rel:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_rel)
            df_tatam:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_tatam)
            df_tcs:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name_tcs)
            print(df_br)
            logging.info("Save data in feature store")

            # Save data in feature store
            logging.info("Create feature store folder if not available")
            #Create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info("Save df to feature store folder")
            # Save df to feature store folder
            df_br.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            df_itc.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            df_rel.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            df_tatam.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            df_tcs.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("split datasets into train and test set")
            # split dataset into train and test set
            train_df_br, test_df_br = split_data(df_br, self.data_ingestion_config.test_size)
            train_df_itc, test_df_itc = split_data(df_itc, self.data_ingestion_config.test_size)
            train_df_rel, test_df_rel = split_data(df_rel, self.data_ingestion_config.test_size)
            train_df_tatam, test_df_tatam = split_data(df_tatam, self.data_ingestion_config.test_size)
            train_df_tcs, test_df_tcs = split_data(df_tcs, self.data_ingestion_config.test_size)
            
            logging.info("create dataset directory folder if not available")
            # Create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving train df and test df to dataset folder")
            # Saving train df and test df to dataset folder
            train_df_br.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df_br.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            train_df_itc.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df_itc.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            train_df_rel.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df_rel.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            train_df_tatam.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df_tatam.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            train_df_tcs.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df_tcs.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            # Prepare artifact  

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise InvestmentPredictionException(error_message=e, error_detail=sys)



        
