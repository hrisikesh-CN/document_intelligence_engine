import os
import sys
from sys import path

from urllib3.util import url

from src.exception import CustomException
from src.utils import *
from src.logger import get_logger
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import uuid
from botocore.exceptions import ClientError


class S3Handler:
    def __init__(self, bucket_name: str,
                 region_name: str = 'us-east-2'):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name.lower()
        self.region_name = region_name
        self.logger = get_logger(__name__)

    def check_bucket_exists(self, bucket_name):
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404' or error_code == '403':
                return False
            else:
                raise e

    def create_unique_bucket_name(self, base_name):
        while True:
            unique_suffix = uuid.uuid4().hex[:8]
            unique_bucket_name = f"{base_name}-{unique_suffix}"
            if not self.check_bucket_exists(unique_bucket_name):
                return unique_bucket_name

    def create_and_get_response_from_s3(self, bucket_name):
        s3_response = self.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': self.region_name}
        )
        self.logger.info(f'Bucket {self.bucket_name} created.')

        return s3_response

    def create_bucket(self):
        try:

            response = self.create_and_get_response_from_s3(self.bucket_name)

            # if response["response"]["ResponseMetadata"]["HTTPStatusCode"] == 200:
            #     return True

        except ClientError as e:
            # if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            #     self.logger.info(f'Bucket {self.bucket_name} already exists.')
            #     return True

            if e.response['Error']['Code'] == 'BucketAlreadyExists' or \
                    e.response['Error']['Code'] == 'IllegalLocationConstraintException':
                unique_bucket_name = self.create_unique_bucket_name(self.bucket_name)
                self.bucket_name = unique_bucket_name
                response = self.create_and_get_response_from_s3(self.bucket_name)
                self.logger.info(
                    f'Bucket {self.bucket_name} is not available. The name was modified by system as {unique_bucket_name}')

                # if response["response"]["ResponseMetadata"]["HTTPStatusCode"] == 200:
                #     return True

            else:
                raise e

        except Exception as e:
            self.logger.info(f"error creating bucket {self.bucket_name}--error message{e}")
            raise CustomException(e, sys)

    def upload_files(self, files):
        responses = []

        if not self.check_bucket_exists(self.bucket_name):
            self.create_bucket()

        for file in files:
            try:
                file_name = file.filename.lower().replace(" ", "-").strip()
                self.s3.upload_fileobj(
                    file,
                    self.bucket_name,
                    file_name
                    ,
                )
                file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
                responses.append({
                    'filename': file.filename,
                    'status': 'success',
                    'url': file_url
                })
            except NoCredentialsError:
                responses.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': 'No AWS credentials found.'
                })
            except PartialCredentialsError:
                responses.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': 'Incomplete AWS credentials found.'
                })
            except Exception as e:
                responses.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': str(e)
                })
        return {'status': 'success', 'results': responses}

    # Flask app to use the S3Uploader
    @staticmethod
    def download_file_from_s3(bucket_name, object_key, local_file_path: str):
        """
        This functions downloads the files from s3 bucket.

        :param file_s3_url:
        :param local_file_path: local path of the downloaded. File name with ext is needed.

        """
        try:
            s3 = boto3.client('s3')

            s3.download_file(bucket_name, object_key, local_file_path)
            print(f"File downloaded from S3 bucket {bucket_name} with key {object_key} to {local_file_path}")
        except Exception as e:
            print(f"Error downloading file from S3: {e}")
