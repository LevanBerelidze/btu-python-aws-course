from cgitb import handler
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

def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]

def main():
    args = parse_args()
    client = boto3.client('lambda')

    with TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'lambda_code.zip')
        file_name = os.path.basename(args.code)

        with ZipFile(file_path, 'w') as zip_file:
            zip_file.write(args.code, file_name)
            
        with open(file_path, 'rb') as zip_file:
            zip_bytes = zip_file.read()
            file_name_without_extension = remove_file_extension(file_name)
            handler_name = f'{file_name_without_extension}.{args.handler}'

            response = client.create_function(
                FunctionName=args.name,
                Runtime='python3.9',
                Role=args.role,
                Handler=handler_name,
                Code={
                    'ZipFile': zip_bytes
                }
            )
            function_arn = response['FunctionArn']
            print(f'Successfully created lambda function. ARN is: {function_arn}')

if __name__ == '__main__':
    main()