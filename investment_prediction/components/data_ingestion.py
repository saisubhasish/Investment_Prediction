from investment_prediction import utils
from investment_prediction.entity import config_entity, artifact_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from investment_prediction.utils import split_data
import os,sys
import pandas as pd 
import numpy as np
collection_name = 'itc'

class DataIngestion:
    
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig ):
        '''
        Storing the input to a variable to use in pipeline
        '''
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            logging.info(f"{'--'*20}Building model for {collection_name}{'--'*20}")
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
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)
            print(df)

            logging.info("Save data in feature store")
            logging.info("Create Feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            
            logging.info("Save df to feature store folder ==>> Dataset")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            
            logging.info("Preparing data ingestion artifacts") 
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path)
                #train_file_path=self.data_ingestion_config.train_file_path_br, 
                #test_file_path=self.data_ingestion_config.test_file_path_br

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise InvestmentPredictionException(error_message=e, error_detail=sys)



        
