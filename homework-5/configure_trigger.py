import boto3
import uuid
from argparse import ArgumentParser

def main():
    args = parse_args()
    grant_permission(args.function, args.bucket)
    add_trigger(args.function, args.bucket)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--function', type=str, required=True)
    args = parser.parse_args()
    return args

def grant_permission(lambda_name, bucket_name):
    lambda_client = boto3.client('lambda')
    lambda_client.add_permission(
        FunctionName=lambda_name,
        StatementId=generate_statement_id(),
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}'
    )

def generate_statement_id():
    return uuid.uuid4().hex

def add_trigger(lambda_arn, bucket_name):
    s3 = boto3.client('s3')
    s3.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': lambda_arn,
                    'Events': ['s3:ObjectCreated:*'],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': '.jpeg'
                                }
                            ]
                        }
                    }
                }
            ],
        }
    )

if __name__ == '__main__':
    main()