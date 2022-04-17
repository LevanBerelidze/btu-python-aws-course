import boto3

from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    parsed_args = parser.parse_args()
    bucket_name = parsed_args.bucket
    return bucket_name

def bucket_exists(s3, bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError:
        return False
    
    return response["ResponseMetadata"]["HTTPStatusCode"] == 200

def main():
    bucket_name = parse_bucket_name()
    s3 = boto3.client('s3')
    
    if bucket_exists(s3, bucket_name):
        print(f'The bucket with name "{bucket_name}" already exists')
    else:
        print(f'Creating bucket "{bucket_name}"...')
        s3.create_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" has been created successfully')

if __name__ == '__main__':
    main()