import mimetypes
import boto3
import os

from argparse import ArgumentParser
from botocore.config import Config
from pprint import pprint

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-d', '--dir', type=str, required=True)
    args = parser.parse_args()
    return args

def guess_content_type(file_path):
    mimetype, _ = mimetypes.guess_type(file_path)
    if mimetype is None:
        return 'binary/octet-stream'
    return mimetype

def upload_directory(s3, dir, bucket):
    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = file_path.replace(f'{dir}{os.sep}', '').replace(os.sep, '/')
            content_type = guess_content_type(file_path)

            print(f'Uploading {file_path}...')
            s3.upload_file(file_path, bucket, file_name, ExtraArgs={ 'ContentType': content_type })
    
    print(f'Fully uploaded directory "{dir}" to bucket "{bucket}"')

def main():
    args = parse_args()
    s3 = boto3.client('s3')
    upload_directory(s3, args.dir, args.bucket)

if __name__ == '__main__':
    main()
