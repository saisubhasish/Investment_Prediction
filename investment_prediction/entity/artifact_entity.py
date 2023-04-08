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