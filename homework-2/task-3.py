import boto3

from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)        
    parsed_args = parser.parse_args()
    bucket_name = parsed_args.name
    return bucket_name

def bucket_exists(s3, bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError:
        return False
    
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    return status_code == 200

def main():
    bucket_name = parse_bucket_name()
    s3 = boto3.client('s3')
    
    if bucket_exists(s3, bucket_name):
        print(f'Deleting bucket with name "{bucket_name}"...')
        
        try:
            s3.delete_bucket(Bucket=bucket_name)
            print(f'Bucket "{bucket_name}" has been deleted successfully')
        except Exception as e:
            print(f'Failed to delete bucket "{bucket_name}": ', e)
    else:
        print(f'Bucket "{bucket_name}" does not exist')

if __name__ == '__main__':
    main()
