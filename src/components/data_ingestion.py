from typing import Union, List
import os, sys
from src.cloud_storage.aws_storage import S3Handler
from src.entity.config_entity import FileHandlerConfig
from src.logger import get_logger
from src.exception import CustomException
class DataIngestion:
    def __init__(self,
                 file_handler_config: FileHandlerConfig):
        self.logger = get_logger(__name__)
        self.file_handler_config = file_handler_config



    def download_data_from_s3(self,
                              urls: Union[str, List[str]]):
        try:
            #download files from s3


        except Exception as e:
            raise CustomException(e, sys)


