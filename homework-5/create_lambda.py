import os
import boto3
from argparse import ArgumentParser
from zipfile import ZipFile
from tempfile import TemporaryDirectory

def main():
    args = parse_args()
    create_lambda(args.name, args.role, args.code, args.handler)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--role', type=str, required=True)
    parser.add_argument('-n', '--name', type=str, required=True)
    parser.add_argument('-c', '--code', type=str, required=True)
    parser.add_argument('-f', '--handler', type=str, required=False, default='lambda_handler')
    args = parser.parse_args()
    return args

def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]

def create_lambda(lambda_name: str, role_arn: str, lambda_code_path: str, lambda_handler_name: str) -> str:
    """
    Creates a lamda function and returns the ARN of the created resource.
    """

    client = boto3.client('lambda')

    with TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'lambda_code.zip')
        file_name = os.path.basename(lambda_code_path)

        with ZipFile(file_path, 'w') as zip_file:
            zip_file.write(lambda_code_path, file_name)
            
        with open(file_path, 'rb') as zip_file:
            zip_bytes = zip_file.read()
            file_name_without_extension = remove_file_extension(file_name)
            handler_name = f'{file_name_without_extension}.{lambda_handler_name}'

            response = client.create_function(
                FunctionName=lambda_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler=handler_name,
                Code={
                    'ZipFile': zip_bytes
                }
            )
            function_arn = response['FunctionArn']
            return function_arn

if __name__ == '__main__':
    main()