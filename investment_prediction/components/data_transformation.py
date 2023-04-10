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
from investment_prediction.config import time_horizon, no_of_features

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
    def scale_feature(cls, trainX, testX):
        try:
            scalers = {}
            for i in range (trainX.shape[2]):
                print(i)
                scalers[i] = StandardScaler()
                trainX[:, :, i] = scalers[i].fit_transform(trainX[:, :, i])
            for i in range(testX.shape[2]):
                testX[:, :, i] = scalers[i].transform(testX[:, :, i])
            return trainX, testX
        
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
            data_combined_train = utils.load_numpy_array_data(self.data_validation_artifact.combined_train_file_path)
            train_data_br = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path_br)
            train_data_itc = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path_itc)
            train_data_rel = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path_rel)
            train_data_tatam = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path_tatam)
            train_data_tcs = utils.load_numpy_array_data(self.data_validation_artifact.train_file_path_tcs)

            data_combined_test = utils.load_numpy_array_data(self.data_validation_artifact.combined_test_file_path)
            test_data_br = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path_br)
            test_data_itc = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path_itc)
            test_data_rel = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path_rel)
            test_data_tatam = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path_tatam)
            test_data_tcs = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path_tcs)
            
            logging.info("Getting the X and Y of each dataset using no. of features and time horizon")
            combined_train_X, combined_train_y  = utils.supvervisedSeries(data_combined_train, no_of_features, time_horizon)   
            combined_test_X, combined_test_y = utils.supvervisedSeries(data_combined_test, no_of_features, time_horizon)

            br_train_X, br_train_y = utils.supvervisedSeries(train_data_br, no_of_features, time_horizon)
            br_test_X, br_test_y = utils.supvervisedSeries(test_data_br, no_of_features, time_horizon)

            itc_train_X, itc_train_y = utils.supvervisedSeries(train_data_itc, no_of_features, time_horizon)
            itc_test_X, itc_test_y = utils.supvervisedSeries(test_data_itc, no_of_features, time_horizon)

            rel_train_X, rel_train_y = utils.supvervisedSeries(train_data_rel, no_of_features, time_horizon)
            rel_test_X, rel_test_y = utils.supvervisedSeries(test_data_rel, no_of_features, time_horizon)

            tatam_train_X, tatam_train_y = utils.supvervisedSeries(train_data_tatam, no_of_features, time_horizon)
            tatam_test_X, tatam_test_y = utils.supvervisedSeries(test_data_tatam, no_of_features, time_horizon)

            tcs_train_X, tcs_train_y = utils.supvervisedSeries(train_data_tcs, no_of_features, time_horizon)
            tcs_test_X, tcs_test_y = utils.supvervisedSeries(test_data_tcs, no_of_features, time_horizon)

            logging.info("Reshaping the Y data of combined data")
            combined_train_y = utils.reshape_Y(combined_train_y)
            combined_test_y = utils.reshape_Y(combined_test_y)

            logging.info("Reshaping the Y data of britannia data")
            br_train_y = utils.reshape_Y(br_train_y)
            br_test_y = utils.reshape_Y(br_test_y)

            logging.info("Reshaping the Y data of itc data")
            itc_train_y = utils.reshape_Y(itc_train_y)
            itc_test_y = utils.reshape_Y(itc_test_y)

            logging.info("Reshaping the Y data of reliance data")
            rel_train_y = utils.reshape_Y(rel_train_y)
            rel_test_y = utils.reshape_Y(rel_test_y)

            logging.info("Reshaping the Y data of tatamotors data")
            tatam_train_y = utils.reshape_Y(tatam_train_y)
            tatam_test_y = utils.reshape_Y(tatam_test_y)

            logging.info("Reshaping the Y data of tcs data")
            tcs_train_y = utils.reshape_Y(tcs_train_y)
            tcs_test_y = utils.reshape_Y(tcs_test_y)

            logging.info("Transforming features of combined data") 
            combined_train_arr_X, combined_test_arr_X = self.scale_feature(combined_train_X, combined_test_X)  # Transformaing input features to array

            logging.info("Transforming features of combined data") 
            br_train_arr_X, br_test_arr_X = self.scale_feature(br_train_X, br_test_X)  # Transformaing input features to array

            logging.info("Transforming features of combined data") 
            itc_train_arr_X, itc_test_arr_X = self.scale_feature(itc_train_X, itc_test_X)  # Transformaing input features to array

            logging.info("Transforming features of combined data") 
            rel_train_arr_X, rel_test_arr_X = self.scale_feature(rel_train_X, rel_test_X)  # Transformaing input features to array

            logging.info("Transforming features of combined data") 
            tatam_train_arr_X, tatam_test_arr_X = self.scale_feature(tatam_train_X, tatam_test_X)  # Transformaing input features to array

            logging.info("Transforming features of combined data") 
            tcs_train_arr_X, tcs_test_arr_X = self.scale_feature(tcs_train_X, tcs_test_X)  # Transformaing input features to array

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(combined_train_y)

            logging.info("Transforming  labels of combined data")
            combined_train_arr_y = transformation_pipleine.transform(combined_train_y)  # Transformaing output label to array
            combined_test_arr_y = transformation_pipleine.transform(combined_test_y)
            
            logging.info("Transforming  labels of britannia data")
            br_train_arr_y = transformation_pipleine.transform(br_train_y)  # Transformaing output label to array
            br_test_arr_y = transformation_pipleine.transform(br_test_y)

            logging.info("Transforming  labels of itc data")
            itc_train_arr_y = transformation_pipleine.transform(itc_train_y)  # Transformaing output label to array
            itc_test_arr_y = transformation_pipleine.transform(itc_test_y)

            logging.info("Transforming  labels of reliance data")
            rel_train_arr_y = transformation_pipleine.transform(rel_train_y)  # Transformaing output label to array
            rel_test_arr_y = transformation_pipleine.transform(rel_test_y)

            logging.info("Transforming  labels of tatamotors data")
            tatam_train_arr_y = transformation_pipleine.transform(tatam_train_y)  # Transformaing output label to array
            tatam_test_arr_y = transformation_pipleine.transform(tatam_test_y)

            logging.info("Transforming  labels of tcs data")
            tcs_train_arr_y = transformation_pipleine.transform(tcs_train_y)  # Transformaing output label to array
            tcs_test_arr_y = transformation_pipleine.transform(tcs_test_y)



            # Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            # Saving object
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipleine)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj=label_encoder)

            # Preparing Artifact
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise InvestmentPredictionException(e, sys)
