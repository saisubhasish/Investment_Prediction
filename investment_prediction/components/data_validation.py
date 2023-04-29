import os,sys 
import pandas as pd
import numpy as np
from typing import Optional
from scipy.stats import ks_2samp     # Compares the continuous distribution of two independent columns

from investment_prediction.entity import artifact_entity,config_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from investment_prediction import utils
from investment_prediction.config import collection_name
from investment_prediction.predictor import ModelResolver


class DataValidation:

    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
            
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
            self.model_resolver = ModelResolver(data_registry=self.data_validation_config.saved_dataset_dir)

        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        """
        This function checks if required columns exists or not by comparing current df with base df and returns
        output as True and False
        """
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:    
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    missing_columns.append(base_column)

            # Return False if there are missing columns in current df other wise True
            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False    
            return True
            
        except Exception as e:
            raise InvestmentPredictionException(e, sys)
            
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        """
        This function checks the data drift in the dataset by comparing current data with base data
        """
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                # Null hypothesis : Both column data has same distribution
                
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)   # Comparing the continuous distribution

                if same_distribution.pvalue>0.05:
                    # We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    # Different distribution                    
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info("Reading base dataframe")
            base_df_br = pd.read_csv(self.data_validation_config.base_file_path_britannia)
            base_df_itc = pd.read_csv(self.data_validation_config.base_file_path_itc)
            base_df_rel = pd.read_csv(self.data_validation_config.base_file_path_reliance)
            base_df_tatam = pd.read_csv(self.data_validation_config.base_file_path_tata_motors)
            base_df_tcs = pd.read_csv(self.data_validation_config.base_file_path_tata_consultancy_services)

            base = self.data_ingestion_artifact.feature_store_file_path
            base = base.split('\\')

            if 'britannia-industries.csv' in base:
                base_df = base_df_br
            elif 'itc.csv' in base:
                base_df = base_df_itc
            elif 'reliance-industries.csv' in base:
                base_df = base_df_rel
            elif 'tata-motors-ltd.csv' in base:
                base_df = base_df_tatam
            elif 'tata-consultancy-services.csv' in base:
                base_df = base_df_tcs

            logging.info("Reading data from data ingestion artifact")
            curr_df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)

            logging.info(f"Is all required columns present in the {collection_name} df")
            df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=curr_df, report_key_name="missing_columns_within_tcs_dataset")
            
            if df_columns_status:     # If True
                logging.info("\n As all column are available in britannia df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=curr_df, report_key_name= f"data_drift_within_{collection_name}_dataset")

            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_validation_config.curr_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            curr_df.to_csv(path_or_buf=self.data_validation_config.curr_file_path, index=False, header=True)

            logging.info("If saved dataset folder has dataset then we will use this validated data for prediction pipeline")
            # Saving dataset outside of artifact
            latest_dir_path = self.model_resolver.get_latest_dataset_dir_path()
            if latest_dir_path==None:    
                logging.info("# There is no saved_dataset, hence saving the current data")      
                print("Saving the current dataset")                        
                
            print("Getting or fetching the directory location to save latest dataset in different directory in each run")
            logging.info("Saving datset in saved dataset dir")
            dataset_path = self.model_resolver.get_latest_save_datset_path()

            print("Saving dataset outside artifact to use in prediction pipeline")
            logging.info('Saving dataset outside of artifact directory')
            curr_df.to_csv(path_or_buf=dataset_path, index=False, header=True)

            logging.info(f"Considering 'Date' and 'Price' column for {collection_name} dataframe")
            df = curr_df[['Date', 'Price']]

            logging.info("Setting 'Date' column as index")
            df = utils.set_index_as_Date(df=df)
            print(df)

            logging.info("split datasets into train and test set")
            train_set, test_set = utils.split_data(df, self.data_validation_config.test_size)

            logging.info("Saving train data and test data")
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path, array=train_set)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path, array=test_set)
            
            print("Writing the report")
            logging.info("Writing report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)   # valiadtion_error: drop columns, missing columns, drift report

            logging.info("Preparing data validation artifacts") 
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,
                                                                              curr_file_path=self.data_validation_config.curr_file_path,
                                                                              train_file_path=self.data_validation_config.train_file_path,
                                                                              test_file_path=self.data_validation_config.test_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise InvestmentPredictionException(e, sys)