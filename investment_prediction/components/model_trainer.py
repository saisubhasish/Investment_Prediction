
from investment_prediction.entity import artifact_entity,config_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from typing import Optional
import os,sys 
from investment_prediction import utils
from sklearn.metrics import f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Dense


class ModelTrainer:

        def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
            try:
                logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
                self.model_trainer_config=model_trainer_config
                self.data_transformation_artifact=data_transformation_artifact

            except Exception as e:
                raise InvestmentPredictionException(e, sys)
            
        def train_model(self,trainX,trainY):
            """
            Model training
            """
            try:
                logging.info("Creating multilayered FFNN model")
                model = Sequential()
                model.add(Dense(100, activation='relu', input_dim=trainX.shape[1]))
                #model.add(Dropout(0.2))
                model.add(Dense(100, activation='relu'))
                #model.add(Dropout(0.2))
                model.add(Dense(100, activation='relu'))
                model.add(Dense(trainY.shape[1]))
                model.compile(loss='mean_squared_error', optimizer='adam')

                logging.info("Fitting model with 60 epochs")
                history = model.fit(trainX, trainY, epochs =60, verbose =1)

                return model

            except Exception as e:
                raise InvestmentPredictionException(e, sys)

        def initiate_model_trainer(self,) -> artifact_entity.ModelTrainerArtifact:
            try:
                logging.info("Reading data from data transformation artifact")
                combined_train_arr_X = self.data_transformation_artifact.transformed_combined_train_arr_X_path
                combined_train_arr_y = self.data_transformation_artifact.transformed_combined_train_arr_y_path
                combined_test_arr_X = self.data_transformation_artifact.transformed_combined_test_arr_X_path
                combined_test_arr_y = self.data_transformation_artifact.transformed_combined_test_arr_y_path

                logging.info("Flatterning the input")
                combined_train_arr_X = utils.flattern_input(combined_train_arr_X)
                combined_test_arr_X = utils.flattern_input(combined_test_arr_X)

                logging.info("Train the model")
                model = self.train_model(trainX = combined_train_arr_X,trainY = combined_train_arr_y)

                y_pred_train = model.predict(combined_train_arr_X)

                y_pred_test = model.predict(combined_test_arr_X)

            except Exception as e:
                raise InvestmentPredictionException(e, sys)