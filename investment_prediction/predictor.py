import os, sys
from investment_prediction.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME
from glob import glob
from typing import Optional
from investment_prediction.exception import InvestmentPredictionException

class ModelResolver:
    """
    This class is helping us to get the location of required updated files (where to save the model 
    and from where to load the model) for prediction pipeline
    """
    def __init__(self,model_registry:str = "saved_models",
                transformer_dir_name="transformer",
                model_dir_name = "model",
                data_registry:str="saved_datasets"):

        self.model_registry=model_registry
        os.makedirs(self.model_registry,exist_ok=True)       # Making directory if not exists
        self.transformer_dir_name = transformer_dir_name
        self.model_dir_name=model_dir_name
        self.data_registry=data_registry
        os.makedirs(self.data_registry,exist_ok=True)       # Making directory if not exists


    def get_latest_dir_path(self)->Optional[str]:
        """
        This function returns None if there is no saved_models present
        Otherwise returns the path of the latest saved_models directory
        """
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_model_path(self):
        """
        This function raise Exception if there is no model present in saved models dir
        Otherwise returns the path of the latest model present in saved_models directory
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Model is not available")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_transformer_path(self):
        """
        This function raise Exception if there is no Transformer present in saved models dir
        Otherwise returns the path of the latest Transformer present in saved_models directory
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_save_dir_path(self)->str:
        """
        This function returns 0 if there is no saved_models dir present
        Otherwise return by adding a number to pre-exist directory 
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir==None:  # If there is no pre-exist directory then create a directory as 0
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}") # Otherwise creating a directory with a number addition
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_save_model_path(self):
        """
        This function extracts the latest saved_models directory and returns the path to save the latest model
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_save_transformer_path(self):
        """
        This function extracts the latest saved_models directory and returns the path to save the latest Transformer
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_dataset_dir_path(self)->Optional[str]:
        """
        This function returns None if there is no dataset present
        Otherwise returns the path of the latest saved dataset directory
        """
        try:
            dir_names = os.listdir(self.data_registry)
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.data_registry,f"{latest_dir_name}")
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_data_path(self):
        """
        This function raise Exception if there is no dataset present in saved datasets dir
        Otherwise returns the path of the latest trained dataset present in saved_datasets directory
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Dataset is not available")
            return os.path.join(latest_dir,self.data,FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

    def get_latest_save_model_path(self):
        """
        This function extracts the latest saved_models directory and returns the path to save the latest model
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise InvestmentPredictionException(e, sys)