from pprint import pprint
import boto3
import uuid
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--function', type=str, required=True)
    args = parser.parse_args()
    return args


{
  "Sid": "AllowToBeInvoked",
  "Effect": "Allow",
  "Principal": {
    "Service": "s3.amazonaws.com"
  },
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:ap-northeast-1:123456789101:function:TestFunc:dev",
  "Condition": {
    "StringEquals": {
      "AWS:SourceAccount": "123456789101"
    },
    "ArnLike": {
      "AWS:SourceArn": "arn:aws:s3:::MyAwesomeBucket"
    }
  }
}

def generate_statement_id():
    return uuid.uuid4().hex

def main():
    args = parse_args()

    lambda_client = boto3.client('lambda')
    add_permission_response = lambda_client.add_permission(
        FunctionName=args.function,
        StatementId=generate_statement_id(),
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{args.bucket}'
    )
    print(f'Granted bucket "{args.bucket}" the permission to invoke lambda function')
    pprint(add_permission_response)

    s3 = boto3.client('s3')
    s3.put_bucket_notification_configuration(
        Bucket=args.bucket,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': args.function,
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
    print('Successfully configured trigger')

if __name__ == '__main__':
    main()