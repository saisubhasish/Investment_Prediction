import os, sys
from investment_prediction.logger import logging
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.config import company_list, raw_file_path, preprocessed_file_path
from ETL.scrapper import Data_scraper
from ETL.data_preprocessing import Data_Wrangling
from ETL.data_dump import Data_Loading
from investment_prediction.config import DATABASE_NAME, COLLECTION_NAME_br, COLLECTION_NAME_itc, COLLECTION_NAME_rel, COLLECTION_NAME_tatam, COLLECTION_NAME_tcs

start_date = '2016-03-19'
end_date = '2023-03-19'
driver_path = r"D:\FSDS-iNeuron\10.Projects-DS\Investment_Prediction\selenium\chromedriver.exe"


def start_data_pipeline():
    try:
        # Data Scrapping
        list(map(lambda company: Data_scraper.scraper(company, start_date, end_date, driver_path, raw_file_path), company_list))

        # Data Pre-processing
        Data_Wrangling.data_cleaning(raw_file_path, preprocessed_file_path)

        # Storing data to mongoDB
        Data_Loading.dump(preprocessed_file_path, DATABASE_NAME, COLLECTION_NAME_br, COLLECTION_NAME_itc, COLLECTION_NAME_rel, COLLECTION_NAME_tatam, COLLECTION_NAME_tcs)

    except Exception as e:
        raise InvestmentPredictionException(e, sys)
