from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    dataset1_file_path:str
    dataset2_file_path:str
    dataset3_file_path:str
    dataset4_file_path:str
    dataset5_file_path:str
    
@dataclass
class DataValidationArtifact:
    report_file_path:str
    combined_file_path:str
    combined_train_file_path:str
    combined_test_file_path:str
    train_file_path_br:str
    train_file_path_itc:str
    train_file_path_rel:str
    train_file_path_tatam:str
    train_file_path_tcs:str
    test_file_path_br:str
    test_file_path_itc:str
    test_file_path_rel:str
    test_file_path_tatam:str
    test_file_path_tcs:str

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

    