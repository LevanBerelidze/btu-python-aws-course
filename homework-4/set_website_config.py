import boto3

from argparse import ArgumentParser
from botocore.config import Config
from pprint import pprint

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    parsed_args = parser.parse_args()
    return parsed_args.bucket

def get_bucket_region(s3, bucket_name):
    region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    region = region if region is not None else 'us-east-1'
    return region

def get_website_url(s3, bucket_name):
    region = get_bucket_region(s3, bucket_name)
    url = f'http://{bucket_name}.s3-website-{region}.amazonaws.com'
    return url

def set_website_config(s3, bucket_name):
    response = s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        }
    )

    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code == 200:
        print('Successfully set website config')
        website_url = get_website_url(s3, bucket_name)
        print(f'Website url: {website_url}')
    else:
        print('Unable to update bucket config, response:')
        pprint(response)

def main():
    bucket_name = parse_bucket_name()
    s3 = boto3.client('s3')
    set_website_config(s3, bucket_name)

if __name__ == '__main__':
    main()
