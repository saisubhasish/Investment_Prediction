import os, sys
from investment_prediction.logger import logging
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.config import raw_file_path, preprocessed_file_path
from ETL.scrapper import Data_scraper
from ETL.data_preprocessing import Data_Wrangling
from ETL.data_dump import Data_Loading


def start_data_pipeline(DATABASE_NAME, start_date, end_date, driver_path, company_list):
    try:
        # Data Scrapping
        list(map(lambda company: Data_scraper.scraper(company, start_date, end_date, driver_path, raw_file_path), company_list))

        # Data Pre-processing
        Data_Wrangling.data_cleaning(raw_file_path, preprocessed_file_path)

        # Storing data to mongoDB
        Data_Loading.dump(preprocessed_file_path, DATABASE_NAME, company_list)

    except Exception as e:
        raise InvestmentPredictionException(e, sys)
