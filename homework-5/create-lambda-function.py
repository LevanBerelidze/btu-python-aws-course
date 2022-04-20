from zipfile import ZipFile
import os
import boto3
from argparse import ArgumentParser
from tempfile import TemporaryDirectory

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--role', type=str, required=True)
    parser.add_argument('-n', '--name', type=str, required=True)
    parser.add_argument('-c', '--code', type=str, required=True)
    parser.add_argument('-m', '--handler', type=str, required=False, default='lambda_handler')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    client = boto3.client('lambda')

    with TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'lambda_code.zip')

        with ZipFile(file_path, 'w') as zip_file:
            zip_file.write(args.code, os.path.basename(args.code))
            
        with open(file_path, 'rb') as zip_file:
            zip_bytes = zip_file.read()
            response = client.create_function(
                FunctionName=args.name,
                Runtime='python3.9',
                Role=args.role,
                Handler=args.handler,
                Code={
                    'ZipFile': zip_bytes
                }
            )
            function_arn = response['FunctionArn']
            print(f'Successfully created lambda function. ARN is: {function_arn}')

if __name__ == '__main__':
    main()