from flask import Flask, request
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class S3Uploader:
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
                file_name=file.filename.lower().replace(" ","-").strip()
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

