import pymongo
import pandas as pd
import json 
from dataclasses import dataclass
import os


start_date = '2016-03-19'
end_date = '2023-03-19'
driver_path = r"D:\FSDS-iNeuron\10.Projects-DS\Investment_Prediction\selenium\chromedriver.exe"
raw_file_path = os.path.join(os.getcwd(),"raw_dataset")
preprocessed_file_path = os.path.join(os.getcwd(),"pre_processed_dataset")

# britannia-industries --> Britannia Inductries
# itc --> ITC
# reliance-industries --> Reliance Industries   
# tata-motors-ltd --> TATA Motors
# tata-consultancy-services  -->  TCS
company_list = ['britannia-industries', 'itc', 'reliance-industries', 'tata-motors-ltd', 'tata-consultancy-services']

DATABASE_NAME="TimeSeries"

COLLECTION_NAME_br="britannia"
COLLECTION_NAME_itc = 'itc'
COLLECTION_NAME_rel = 'reliance'
COLLECTION_NAME_tatam = 'tatamotors'
COLLECTION_NAME_tcs = 'tcs'

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
TARGET_COLUMN = ""