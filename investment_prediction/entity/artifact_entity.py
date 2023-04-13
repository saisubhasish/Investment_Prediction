from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    
@dataclass
class DataValidationArtifact:
    report_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_combined_train_arr_X_path:str
    transformed_combined_test_arr_X_path:str
    transformed_combined_train_arr_y_path:str
    transformed_combined_test_arr_y_path:str
    transformed_br_train_arr_X_path:str
    transformed_br_test_arr_X_path:str
    transformed_br_train_arr_y_path:str
    transformed_br_test_arr_y_path:str
    transformed_itc_train_arr_X_path:str
    transformed_itc_test_arr_X_path:str
    transformed_itc_train_arr_y_path:str
    transformed_itc_test_arr_y_path:str
    transformed_rel_train_arr_X_path:str
    transformed_rel_test_arr_X_path:str
    transformed_rel_train_arr_y_path:str
    transformed_rel_test_arr_y_path:str
    transformed_tatam_train_arr_X_path:str
    transformed_tatam_test_arr_X_path:str
    transformed_tatam_train_arr_y_path:str
    transformed_tatam_test_arr_y_path:str
    transformed_tcs_train_arr_X_path:str
    transformed_tcs_test_arr_X_path:str
    transformed_tcs_train_arr_y_path:str
    transformed_tcs_test_arr_y_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str 
    f1_train_score:float 
    f1_test_score:float

    