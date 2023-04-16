import os,sys 
from typing import Optional

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from investment_prediction import utils
from investment_prediction.logger import logging
from investment_prediction.entity import artifact_entity,config_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.config import time_step

class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_validation_artifact:artifact_entity.DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise InvestmentPredictionException(e, sys) 
        
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:     # Attributes of this class will be same across all the object 
        try:
            scaler =  StandardScaler()
            pipeline = Pipeline(steps=[
                    ('StandardScaler',scaler)  # To scale data in a range
                ])
            return pipeline
        
        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            logging.info("Reading training and testing file")
            train_data = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path)
            test_data = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path)
            
            logging.info("Standardizing dataset")
            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(train_data)

            logging.info("Transforming dataset")
            train_data_arr = transformation_pipleine.transform(train_data)
            test_data_arr = transformation_pipleine.transform(test_data)
            print(train_data_arr)

            logging.info("Getting the X and Y of each dataset using time step = 60")
            X_train_arr, y_train_arr = utils.create_dataset(train_data_arr, time_step)
            X_test_arr, y_test_arr = utils.create_dataset(test_data_arr, time_step)

            logging.info("Reshaping the X data")
            X_train_arr = utils.reshape_X(X_train_arr)
            X_test_arr =  utils.reshape_X(X_test_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_arr_X_path, array=X_train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_arr_y_path, array=y_train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_arr_X_path, array=X_test_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_arr_y_path, array=y_test_arr)

            print("Saving transformation object")
            logging.info("Saving transformation object")
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipleine)

            logging.info("Preparing Artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,             
                transformed_train_arr_X_path = self.data_transformation_config.transformed_train_arr_X_path,
                transformed_train_arr_y_path = self.data_transformation_config.transformed_train_arr_y_path,
                transformed_test_arr_X_path = self.data_transformation_config.transformed_test_arr_X_path,
                transformed_test_arr_y_path = self.data_transformation_config.transformed_test_arr_y_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise InvestmentPredictionException(e, sys)
