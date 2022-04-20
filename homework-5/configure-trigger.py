import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--function', type=str, required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
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