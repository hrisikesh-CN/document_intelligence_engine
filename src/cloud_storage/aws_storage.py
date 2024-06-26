import os
from sys import path

from urllib3.util import url

from src.utils import *
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


class S3Handler:
    def __init__(self, bucketname):
        self.bucketname = bucketname
        self.s3 = boto3.client(
            's3'
        )

    def bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucketname)
            return True
        except ClientError:
            return False

    def create_bucket(self):
        try:
            self.s3.create_bucket(Bucket=self.bucketname)

            return {'status': 'success', 'message': f'Bucket {self.bucketname} created.'}
        except ClientError as e:
            return {'status': 'error', 'message': str(e)}

    def upload_files(self, files):
        responses = []

        if not self.bucket_exists():
            create_response = self.create_bucket()
            if create_response['status'] == 'error':
                return create_response

        for file in files:
            try:
                file_name = file.filename.lower().replace(" ", "-").strip()
                self.s3.upload_fileobj(
                    file,
                    self.bucketname,
                    file_name
                    ,
                )
                file_url = f"https://{self.bucketname}.s3.amazonaws.com/{file_name}"
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
