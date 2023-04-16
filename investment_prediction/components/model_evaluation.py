from investment_prediction.entity import config_entity, artifact_entity
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.predictor import ModelResolver
from investment_prediction.utils import load_object
from investment_prediction import utils
from sklearn.metrics import r2_score
from investment_prediction.logger import logging
import pandas as pd
import os, sys
from investment_prediction.config import time_step


class ModelEvaluation:

    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_validation_artifact:artifact_entity.DataValidationArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InvestmentPredictionException(e,sys)
        
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            logging.info("If saved model folder has model the we will compare "
            "which model is best, trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:    
                logging.info("# If there is no saved_models then we will accept the currnt model")                             
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)                                                              
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            logging.info("Finding location of transformer model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()

            logging.info("Loading objects")
            logging.info("Previous trained objects of transformer and model")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)            

            logging.info("Currently trained model objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            

            logging.info("Reading test file")
            test_data = utils.load_numpy_array_data(self.data_validation_artifact.test_file_path)

            logging.info("Standardizing test data")
            test_data_arr =transformer.transform(test_data)

            logging.info("Creating X and Y data from test dataset")
            input_arr, y_true = utils.create_dataset(test_data_arr, time_step)
            
            logging.info("Accuracy using previous trained model")
            logging.info("Predicting output")
            y_pred = model.predict(input_arr)

            logging.info("Label decoding with 5 values to get actual string")
            print(f"Prediction using previous model: {transformer.inverse_transform(y_pred[:5])}")
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

            logging.info("Accuracy using current trained model")
            logging.info("Standardizing test data")
            test_data_arr_curr = current_transformer.transform(test_data)
            
            logging.info("Creating X and Y data from test dataset")
            input_arr, y_true = utils.create_dataset(test_data_arr_curr, time_step)

            y_pred = current_model.predict(input_arr)
            logging.info("Label decoding with 5 values to get actual string")
            print(f"Prediction using trained model: {current_transformer.inverse_transform(y_pred[:5])}")
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")

            if current_model_score<=previous_model_score:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            
            # Improved accuracy
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        
        except Exception as e:
            raise InvestmentPredictionException(e,sys)
