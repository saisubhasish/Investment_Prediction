import os,sys 
from typing import Optional
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, LSTM, Dense

from investment_prediction.entity import artifact_entity,config_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging
from investment_prediction import utils



class ModelTrainer:

        def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
            try:
                logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
                self.model_trainer_config=model_trainer_config
                self.data_transformation_artifact=data_transformation_artifact

            except Exception as e:
                raise InvestmentPredictionException(e, sys)
            
        def train_model(self,X_train, y_train):
            """
            Model training
            """
            try:
                model = Sequential()
                model.add(LSTM(units=100, return_sequences = True, input_shape = (X_train.shape[1], 1)))
                model.add(LSTM(units=100, return_sequences = True))
                model.add(Dropout(0.2))
                model.add(LSTM(units=100, return_sequences = True))
                model.add(Dropout(0.2))
                model.add(LSTM(units=100, return_sequences = False))
                model.add(Dense(units=1))
                model.compile(optimizer='adam', loss='mean_squared_error')

                logging.info("Fitting model with 60 epochs")
                history = model.fit(X_train, y_train, epochs=20, batch_size= 32, verbose=2)

                return model

            except Exception as e:
                raise InvestmentPredictionException(e, sys)

        def initiate_model_trainer(self,) -> artifact_entity.ModelTrainerArtifact:
            try:
                logging.info("Reading data from data transformation artifact")
                train_arr_X = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_arr_X_path)
                train_arr_y = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_arr_y_path)
                test_arr_X = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_arr_X_path)
                test_arr_y = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_arr_y_path)

                print("Model Training")
                logging.info("Train the model")
                model = self.train_model(train_arr_X ,train_arr_y)
                
                logging.info("Calculating r2 train score")
                y_pred_train = model.predict(train_arr_X)
                r2_train_score = r2_score(train_arr_y, y_pred_train)

                logging.info("Calculating r2 test score")
                y_pred_test = model.predict(test_arr_X)
                r2_test_score = r2_score(test_arr_y, y_pred_test)

                logging.info(f"train score:{r2_train_score} and tests score {r2_test_score}")
                
                print("Checking if our model is Overfitted pr  underfitted")
                logging.info("Checking if our model is underfitting or not")
                if r2_test_score<self.model_trainer_config.expected_score:
                    raise Exception(f"Model is not good as it is not able to give \
                    expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {r2_test_score}")
                
                logging.info("Checking if our model is overfiiting or not")
                diff = abs(r2_train_score-r2_test_score)   # Checking the difference by removing -ve

                if diff>self.model_trainer_config.overfitting_threshold:
                    raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")
                
                print(f"Train-Test difference: {diff}")
                # Saving trained model using utils if it passes
                logging.info("Saving model object")
                utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

                # Prepare artifact
                logging.info("Prepare the artifact")
                model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
                r2_train_score=r2_train_score, r2_test_score=r2_test_score)
                logging.info(f"Model trainer artifact: {model_trainer_artifact}")
                return model_trainer_artifact


            except Exception as e:
                raise InvestmentPredictionException(e, sys)