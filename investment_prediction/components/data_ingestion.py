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
            logging.info("Create feature store folder if not available")
            feature_store_dir_br = os.path.dirname(self.data_ingestion_config.feature_store_file_path_br)
            os.makedirs(feature_store_dir_br,exist_ok=True)
            feature_store_dir_itc = os.path.dirname(self.data_ingestion_config.feature_store_file_path_itc)
            os.makedirs(feature_store_dir_itc,exist_ok=True)
            feature_store_dir_rel = os.path.dirname(self.data_ingestion_config.feature_store_file_path_rel)
            os.makedirs(feature_store_dir_rel,exist_ok=True)
            feature_store_dir_tatam = os.path.dirname(self.data_ingestion_config.feature_store_file_path_tatam)
            os.makedirs(feature_store_dir_tatam,exist_ok=True)
            feature_store_dir_tcs = os.path.dirname(self.data_ingestion_config.feature_store_file_path_tcs)
            os.makedirs(feature_store_dir_tcs,exist_ok=True)

            logging.info("Save df to feature store folder")
            df_br.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path_br, index=False, header=True)
            df_itc.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path_itc, index=False, header=True)
            df_rel.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path_rel, index=False, header=True)
            df_tatam.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path_tatam, index=False, header=True)
            df_tcs.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path_tcs, index=False, header=True)

            logging.info("split datasets into train and test set")
            train_df_br, test_df_br = split_data(df_br, self.data_ingestion_config.test_size)
            train_df_itc, test_df_itc = split_data(df_itc, self.data_ingestion_config.test_size)
            train_df_rel, test_df_rel = split_data(df_rel, self.data_ingestion_config.test_size)
            train_df_tatam, test_df_tatam = split_data(df_tatam, self.data_ingestion_config.test_size)
            train_df_tcs, test_df_tcs = split_data(df_tcs, self.data_ingestion_config.test_size)
            
            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path_br)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving train df and test df to dataset folder")
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.train_file_path_br, array=train_df_br)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.test_file_path_br, array=test_df_br)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.train_file_path_itc, array=train_df_itc)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.test_file_path_itc, array=test_df_itc)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.train_file_path_rel, array=train_df_rel)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.test_file_path_rel, array=test_df_rel)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.train_file_path_tatam, array=train_df_tatam)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.test_file_path_tatam, array=test_df_tatam)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.train_file_path_tcs, array=train_df_tcs)
            utils.save_numpy_array_data(file_path=self.data_ingestion_config.test_file_path_tcs, array=test_df_tcs)
            
            # Prepare artifact  
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path_br,
                train_file_path=self.data_ingestion_config.train_file_path_br, 
                test_file_path=self.data_ingestion_config.test_file_path_br)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise InvestmentPredictionException(error_message=e, error_detail=sys)



        
