import os, sys
from investment_prediction.logger import logging
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.utils import get_collection_as_dataframe
from investment_prediction.entity.config_entity import DataIngestionConfig
from investment_prediction.entity import config_entity, artifact_entity
from investment_prediction.components.data_ingestion import DataIngestion


if __name__ == '__main__':
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # data ingestion         
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        raise InvestmentPredictionException(e, sys)
