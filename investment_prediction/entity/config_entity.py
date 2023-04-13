import os, sys
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from datetime import datetime

collection_name = 'itc'

FILE_NAME = f"{collection_name}.csv"
TRAIN_FILE_NAME = f"{collection_name}_train.npz"
TEST_FILE_NAME = f"{collection_name}_test.npz"

BRITANNIA_TRAIN_ARRAY_X_FILE_NAME = "br_train_arr_X.npz"
BRITANNIA_TEST_ARRAY_X_FILE_NAME = "br_test_arr_X.npz"
BRITANNIA_TRAIN_ARRAY_y_FILE_NAME = "br_train_arr_y.npz"
BRITANNIA_TEST_ARRAY_y_FILE_NAME = "br_test_arr_y.npz"

TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
MODEL_FILE_NAME = "model.h5"


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
            self.collection_name = collection_name
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")    
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store", FILE_NAME)

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

            self.base_file_path_britannia = os.path.join("britannia-industries.csv")
            self.base_file_path_itc = os.path.join("itc.csv")
            self.base_file_path_reliance = os.path.join("reliance-industries.csv")
            self.base_file_path_tata_motors = os.path.join("tata-motors-ltd.csv")
            self.base_file_path_tata_consultancy_services = os.path.join("tata-consultancy-services.csv")

            self.dataset_dir = os.path.join(self.data_validation_dir,"dataset")
            
            self.train_file_path = os.path.join(self.dataset_dir,"Dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.dataset_dir,"Dataset",TEST_FILE_NAME)

            self.test_size = 0.2
            self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")
            
        except Exception  as e:
            raise InvestmentPredictionException(e,sys)  
        
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
            self.transformationed_dir_path = os.path.join(self.data_transformation_dir,"transformed")

            self.transformed_combined_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Combined_dataset",COMBINED_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_combined_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Combined_dataset",COMBINED_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_combined_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Combined_dataset",COMBINED_TEST_ARRAY_X_FILE_NAME)
            self.transformed_combined_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Combined_dataset",COMBINED_TEST_ARRAY_y_FILE_NAME)
            
            self.transformed_br_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_1",BRITANNIA_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_br_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_1",BRITANNIA_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_br_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_1",BRITANNIA_TEST_ARRAY_X_FILE_NAME)
            self.transformed_br_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_1",BRITANNIA_TEST_ARRAY_y_FILE_NAME)

            self.transformed_itc_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_2",ITC_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_itc_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_2",ITC_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_itc_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_2",ITC_TEST_ARRAY_X_FILE_NAME)
            self.transformed_itc_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_2",ITC_TEST_ARRAY_y_FILE_NAME)

            self.transformed_rel_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_3",RELIANCE_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_rel_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_3",RELIANCE_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_rel_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_3",RELIANCE_TEST_ARRAY_X_FILE_NAME)
            self.transformed_rel_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_3",RELIANCE_TEST_ARRAY_y_FILE_NAME)

            self.transformed_tatam_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_4",TATAMOTORS_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_tatam_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_4",TATAMOTORS_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_tatam_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_4",TATAMOTORS_TEST_ARRAY_X_FILE_NAME)
            self.transformed_tatam_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_4",TATAMOTORS_TEST_ARRAY_y_FILE_NAME)

            self.transformed_tcs_train_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_5",TCS_TRAIN_ARRAY_X_FILE_NAME)
            self.transformed_tcs_train_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_5",TCS_TRAIN_ARRAY_y_FILE_NAME)
            self.transformed_tcs_test_arr_X_path = os.path.join(self.transformationed_dir_path,"Dataset_5",TCS_TEST_ARRAY_X_FILE_NAME)
            self.transformed_tcs_test_arr_y_path = os.path.join(self.transformationed_dir_path,"Dataset_5",TCS_TRAIN_ARRAY_y_FILE_NAME)

        except Exception  as e:
            raise InvestmentPredictionException(e,sys) 
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")
            self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
            self.expected_score = 0.7
            self.overfitting_threshold = 0.1
        
        except Exception as e:
            raise InvestmentPredictionException(e,sys)