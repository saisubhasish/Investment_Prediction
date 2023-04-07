import sys
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.pipeline.data_pipeline import start_data_pipeline


if __name__ == '__main__':
    try:
        start_data_pipeline()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)