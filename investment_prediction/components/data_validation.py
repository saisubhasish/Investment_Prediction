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

            logging.info("Reading britannia dataframe")
            curr_df_br = pd.read_csv(self.data_ingestion_artifact.dataset1_file_path)
            logging.info("Reading itc dataframe")
            curr_df_itc = pd.read_csv(self.data_ingestion_artifact.dataset2_file_path)
            logging.info("Reading reliance dataframe")
            curr_df_rel = pd.read_csv(self.data_ingestion_artifact.dataset3_file_path)
            logging.info("Reading tatamotors dataframe")
            curr_df_tatam = pd.read_csv(self.data_ingestion_artifact.dataset4_file_path)
            logging.info("Reading tcs dataframe")
            curr_df_tcs = pd.read_csv(self.data_ingestion_artifact.dataset5_file_path)

            logging.info("Is all required columns present in britannia df")
            df_br_columns_status = self.is_required_columns_exists(base_df=base_df_br, current_df=curr_df_br, report_key_name="missing_columns_within_britannia_dataset")
            logging.info("Is all required columns present in itc df")
            df_itc_columns_status = self.is_required_columns_exists(base_df=base_df_itc, current_df=curr_df_itc, report_key_name="missing_columns_within_itc_dataset")
            logging.info("Is all required columns present in reliance df")
            df_rel_columns_status = self.is_required_columns_exists(base_df=base_df_rel, current_df=curr_df_rel, report_key_name="missing_columns_within_reliance_dataset")
            logging.info("Is all required columns present in tatamotors df")
            df_tatam_columns_status = self.is_required_columns_exists(base_df=base_df_tatam, current_df=curr_df_tatam, report_key_name="missing_columns_within_tatamotors_dataset")
            logging.info("Is all required columns present in tcs df")
            df_tcs_columns_status = self.is_required_columns_exists(base_df=base_df_tcs, current_df=curr_df_tcs, report_key_name="missing_columns_within_tcs_dataset")
            
            if df_br_columns_status:     # If True
                logging.info("\n As all column are available in britannia df hence detecting data drift")
                self.data_drift(base_df=base_df_br, current_df=curr_df_br,report_key_name="data_drift_within_britannia_dataset")

            if df_itc_columns_status:     # If True
                logging.info("\n As all column are available in itc df hence detecting data drift")
                self.data_drift(base_df=base_df_itc, current_df=curr_df_itc,report_key_name="data_drift_within_itc_dataset")

            if df_rel_columns_status:     # If True
                logging.info("\n As all column are available in reliance df hence detecting data drift")
                self.data_drift(base_df=base_df_rel, current_df=curr_df_rel,report_key_name="data_drift_within_reliance_dataset")

            if df_tatam_columns_status:     # If True
                logging.info("\n As all column are available in tatamotors df hence detecting data drift")
                self.data_drift(base_df=base_df_tatam, current_df=curr_df_tatam,report_key_name="data_drift_within_tatamotors_dataset")

            if df_tcs_columns_status:     # If True
                logging.info("\n As all column are available in tcs df hence detecting data drift")
                self.data_drift(base_df=base_df_tcs, current_df=curr_df_tcs,report_key_name="data_drift_within_tcs_dataset")

            logging.info("Considering 'Date' and 'Price' column for britannia dataframe")
            df_br = curr_df_br[['Date', 'Price']]
            logging.info("Considering 'Date' and 'Price' column for itc dataframe")
            df_itc = curr_df_itc[['Date', 'Price']]
            logging.info("Considering 'Date' and 'Price' column for reliance dataframe")
            df_rel = curr_df_rel[['Date', 'Price']]
            logging.info("Considering 'Date' and 'Price' column for tatamotors dataframe")
            df_tatam = curr_df_tatam[['Date', 'Price']]
            logging.info("Considering 'Date' and 'Price' column for tcs dataframe")
            df_tcs = curr_df_tcs[['Date', 'Price']]

            logging.info("Preparing list of dataframes")
            df_list = [df_br, df_itc, df_rel, df_tatam, df_tcs]

            logging.info("Setting 'Date' column as index")
            list(map(utils.set_index_as_Date, df_list))

            logging.info("Preparing combined dataframe")
            df_combined = pd.concat([df_br['Price'], df_itc['Price'], df_rel['Price'], df_tatam['Price'], df_tcs['Price']], axis=1, join="inner", keys= ["Britannia", "ITC", "Reliance", "TATA_Motors", "TCS"])

            logging.info("split datasets into train and test set")
            df_combined_train, df_combined_test = utils.split_data(df_combined, self.data_validation_config.test_size)
            train_df_br, test_df_br = utils.split_data(df_br, self.data_validation_config.test_size)
            train_df_itc, test_df_itc = utils.split_data(df_itc, self.data_validation_config.test_size)
            train_df_rel, test_df_rel = utils.split_data(df_rel, self.data_validation_config.test_size)
            train_df_tatam, test_df_tatam = utils.split_data(df_tatam, self.data_validation_config.test_size)
            train_df_tcs, test_df_tcs = utils.split_data(df_tcs, self.data_validation_config.test_size)
            
            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_validation_config.train_file_path_br)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving train df and test df to dataset folder")
            utils.save_numpy_array_data(file_path=self.data_validation_config.combined_train_file_path, array=df_combined_train)
            utils.save_numpy_array_data(file_path=self.data_validation_config.combined_test_file_path, array=df_combined_test)
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path_br, array=train_df_br)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path_br, array=test_df_br)
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path_itc, array=train_df_itc)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path_itc, array=test_df_itc)
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path_rel, array=train_df_rel)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path_rel, array=test_df_rel)
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path_tatam, array=train_df_tatam)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path_tatam, array=test_df_tatam)
            utils.save_numpy_array_data(file_path=self.data_validation_config.train_file_path_tcs, array=train_df_tcs)
            utils.save_numpy_array_data(file_path=self.data_validation_config.test_file_path_tcs, array=test_df_tcs)
            df_combined.to_csv(path_or_buf=self.data_validation_config.combined_file_path, index=False, header=True)

            # Write the report
            logging.info("Writing report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)   # valiadtion_error: drop columns, missing columns, drift report

            logging.info("Preparing data validation artifacts") 
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,
                                                                              combined_file_path=self.data_validation_config.combined_file_path,
                                                                              combined_train_file_path=self.data_validation_config.combined_train_file_path,
                                                                              combined_test_file_path=self.data_validation_config.combined_test_file_path,
                                                                              train_file_path_br=self.data_validation_config.train_file_path_br,
                                                                              train_file_path_itc=self.data_validation_config.train_file_path_itc,
                                                                              train_file_path_rel=self.data_validation_config.train_file_path_rel,
                                                                              train_file_path_tatam=self.data_validation_config.train_file_path_tatam,
                                                                              train_file_path_tcs=self.data_validation_config.train_file_path_tcs,
                                                                              test_file_path_br=self.data_validation_config.test_file_path_br,
                                                                              test_file_path_itc=self.data_validation_config.test_file_path_itc,
                                                                              test_file_path_rel=self.data_validation_config.test_file_path_rel,
                                                                              test_file_path_tatam=self.data_validation_config.test_file_path_tatam,
                                                                              test_file_path_tcs=self.data_validation_config.test_file_path_tcs)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise InvestmentPredictionException(e, sys)