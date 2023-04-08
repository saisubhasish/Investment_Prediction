import os, sys
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from datetime import datetime

BRITANNIA_FILE_NAME = "britannia.csv"
ITC_FILE_NAME = "itc.csv"
RELIANCE_FILE_NAME = "reliance.csv"
TATAMOTORS_FILE_NAME = "tatamotors.csv"
TCS_FILE_NAME = "tcs.csv"

BRITANNIA_TRAIN_FILE_NAME = "britannia_train.npz"
ITC_TRAIN_FILE_NAME = "itc_train.npz"
RELIANCE_TRAIN_FILE_NAME = "reliance_train.npz"
TATAMOTORS_TRAIN_FILE_NAME = "tatamotors_train.npz"
TCS_TRAIN_FILE_NAME = "tcs_train.npz"

BRITANNIA_TEST_FILE_NAME = "britannia_test.npz"
ITC_TEST_FILE_NAME = "itc_test.npz"
RELIANCE_TEST_FILE_NAME = "reliance_test.npz"
TATAMOTORS_TEST_FILE_NAME = "tatamotors_test.npz"
TCS_TEST_FILE_NAME = "tcs_test.npz"


TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")                        
        except Exception  as e:
            raise InvestmentPredictionException(e,sys)  
        
class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="TimeSeries"

            self.collection_name_br="britannia"
            self.collection_name_itc="itc"
            self.collection_name_rel="reliance"
            self.collection_name_tatam="tatamotors"
            self.collection_name_tcs="tcs"

            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")

            self.feature_store_file_path_br = os.path.join(self.data_ingestion_dir,"feature_store")
            self.feature_store_file_path_itc = os.path.join(self.data_ingestion_dir,"feature_store")
            self.feature_store_file_path_rel = os.path.join(self.data_ingestion_dir,"feature_store")
            self.feature_store_file_path_tatam = os.path.join(self.data_ingestion_dir,"feature_store")
            self.feature_store_file_path_tcs = os.path.join(self.data_ingestion_dir,"feature_store")

            self.dataset1_file_path = os.path.join(self.feature_store_file_path_br,"Dataset_1",BRITANNIA_FILE_NAME)
            self.dataset2_file_path = os.path.join(self.feature_store_file_path_itc,"Dataset_2",ITC_FILE_NAME)
            self.dataset3_file_path = os.path.join(self.feature_store_file_path_rel,"Dataset_3",RELIANCE_FILE_NAME)
            self.dataset4_file_path = os.path.join(self.feature_store_file_path_tatam,"Dataset_4",TATAMOTORS_FILE_NAME)
            self.dataset5_file_path = os.path.join(self.feature_store_file_path_tcs,"Dataset_5",TCS_FILE_NAME)
            
        except Exception  as e:
            raise InvestmentPredictionException(e,sys)        

    def to_dict(self,)->dict:
        """
        To convert and return the output as dict
        """ 
        try:
            return self.__dict__

        except Exception  as e:
            raise InvestmentPredictionException(e,sys)  
        
class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_validation")

            self.base_file_path_br = os.path.join("britannia.csv")
            self.base_file_path_itc = os.path.join("itc.csv")
            self.base_file_path_rel = os.path.join("reliance.csv")
            self.base_file_path_tatam = os.path.join("tatamotors.csv")
            self.base_file_path_tcs = os.path.join("tcs.csv")

            self.dataset_dir = os.path.join(self.data_validation_dir,"dataset")
            
            self.train_file_path_br = os.path.join(self.dataset_dir,"Dataset_1",BRITANNIA_TRAIN_FILE_NAME)
            self.train_file_path_itc = os.path.join(self.dataset_dir,"Dataset_2",ITC_TRAIN_FILE_NAME)
            self.train_file_path_rel = os.path.join(self.dataset_dir,"Dataset_3",RELIANCE_TRAIN_FILE_NAME)
            self.train_file_path_tatam = os.path.join(self.dataset_dir,"Dataset_4",TATAMOTORS_TRAIN_FILE_NAME)
            self.train_file_path_tcs = os.path.join(self.dataset_dir,"Dataset_5",TCS_TRAIN_FILE_NAME)

            self.test_file_path_br = os.path.join(self.dataset_dir,"Dataset_1",BRITANNIA_TEST_FILE_NAME)
            self.test_file_path_itc = os.path.join(self.dataset_dir,"Dataset_2",ITC_TEST_FILE_NAME)
            self.test_file_path_rel = os.path.join(self.dataset_dir,"Dataset_3",RELIANCE_TEST_FILE_NAME)
            self.test_file_path_tatam = os.path.join(self.dataset_dir,"Dataset_4",TATAMOTORS_TEST_FILE_NAME)
            self.test_file_path_tcs = os.path.join(self.dataset_dir,"Dataset_5",TCS_TEST_FILE_NAME)

            self.test_size = 0.2
            self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")
            
        except Exception  as e:
            raise InvestmentPredictionException(e,sys)  