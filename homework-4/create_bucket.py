import boto3

from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    parsed_args = parser.parse_args()
    return parsed_args.bucket

def main():
    bucket_name = parse_bucket_name()
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)
    print(f'Successfully create bucket "{bucket_name}"')

if __name__ == '__main__':
    main()