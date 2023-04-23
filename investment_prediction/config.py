import pymongo
import pandas as pd
import json 
from dataclasses import dataclass
import os


DATABASE_NAME="TimeSeries"
collection_name = 'britannia-industries'
raw_file_path = os.path.join(os.getcwd(),"raw_dataset")
preprocessed_file_path = os.path.join(os.getcwd(),"pre_processed_dataset")

time_step = 7 # the number of time steps of historical data that the model will use to make a single prediction.

@dataclass
class EnvironmentVariable:
    """
    In this class we are accessing the variables declared in .env file
    """
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)