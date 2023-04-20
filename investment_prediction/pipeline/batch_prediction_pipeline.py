import os,sys
import pandas as pd
import numpy as np
from datetime import datetime

from investment_prediction import utils
from investment_prediction.logger import logging
from investment_prediction.utils import load_object
from investment_prediction.entity import config_entity
from investment_prediction.predictor import ModelResolver
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.components.data_validation import DataValidation


PREDICTION_DIR= "prediction"

validation_error=dict()

base_file_path_br = os.path.join("britannia-industries.csv")
base_file_path_itc = os.path.join("itc.csv")
base_file_path_rel = os.path.join("reliance-industries.csv")
base_file_path_tatam = os.path.join("tata-motors-ltd.csv")
base_file_path_tcs = os.path.join("tata-consultancy-services.csv")

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        report_file_dir = os.path.join(PREDICTION_DIR)
        os.makedirs(report_file_dir, exist_ok=True)

        logging.info("Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")   # Location where models are saved

        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)

        # Loading standard scaler
        logging.info("Loading standard scaler object")
        scaler = load_object(file_path=model_resolver.get_latest_transformer_path())

        # data frame
        input_arr = scaler.transform(df)

        # Prediction    
        logging.info("Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        # Inverse Transform  
        logging.info("To convert transformed predicted values to real value")
        predicted_price = model.inverse_transform(prediction)

        

    except Exception as e:
        raise InvestmentPredictionException(e, sys)