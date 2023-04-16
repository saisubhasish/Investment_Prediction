import sys
from investment_prediction.config import DATABASE_NAME
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.pipeline.data_pipeline import start_data_pipeline
from investment_prediction.pipeline.training_pipeline import start_training_pipeline

start_date = '2016-03-19'
end_date = '2023-03-19'
driver_path = r"D:\FSDS-iNeuron\10.Projects-DS\Investment_Prediction\selenium\chromedriver.exe"
company_list = ['britannia-industries', 'itc', 'reliance-industries', 'tata-motors-ltd', 'tata-consultancy-services']


if __name__ == '__main__':
    try:
        start_data_pipeline(DATABASE_NAME, start_date, end_date, driver_path, company_list)
        start_training_pipeline()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)