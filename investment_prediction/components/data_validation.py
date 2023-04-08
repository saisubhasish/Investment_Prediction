from investment_prediction.entity import artifact_entity,config_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from scipy.stats import ks_2samp     # Compares the continuous distribution of two independent columns
from typing import Optional
import os,sys 
import pandas as pd
from investment_prediction import utils
import numpy as np


class DataValidation:


    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
            
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()

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
            base_df_br = pd.read_csv(self.data_validation_config.base_file_path_br)
            base_df_itc = pd.read_csv(self.data_validation_config.base_file_path_itc)
            base_df_rel = pd.read_csv(self.data_validation_config.base_file_path_rel)
            base_df_tatam = pd.read_csv(self.data_validation_config.base_file_path_tatam)
            base_df_tcs = pd.read_csv(self.data_validation_config.base_file_path_tcs)

            

            logging.info("Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)



            logging.info("Is all required columns present in britannia df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df_br, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info("Is all required columns present in itc df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")
            logging.info("Is all required columns present in reliance df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info("Is all required columns present in tatamotors df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")
            logging.info("Is all required columns present in tcs df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")

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

        except Exception as e:
            raise InvestmentPredictionException(e, sys)