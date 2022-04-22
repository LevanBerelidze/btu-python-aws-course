import boto3

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    return parser.parse_args()

def create_bucket(bucket_name: str):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

def main():
    args = parse_args()
    create_bucket(args.bucket)

if __name__ == '__main__':
    main()