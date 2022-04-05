import boto3
import botocore
import json

from pprint import pprint
from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)        
    parsed_args = parser.parse_args()
    bucket_name = parsed_args.name
    return bucket_name

def read_bucket_policy(s3, bucket_name):
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        policy_str = policy["Policy"]
        return json.loads(policy_str)
    except botocore.exceptions.ClientError:
        return None

def generate_public_read_policy(bucket_name, prefixes):
    resources = map(lambda p: f"arn:aws:s3:::{bucket_name}/{p}/*", prefixes)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": list(resources)
            }
        ]
    }

    return json.dumps(policy)

def main():
    bucket_name = parse_bucket_name()
    s3 = boto3.client('s3')

    current_policy = read_bucket_policy(s3, bucket_name)
    if current_policy is None:
        print('Generating new policy...')
        public_policy = generate_public_read_policy(bucket_name, ['dev', 'test'])
        s3.put_bucket_policy(Bucket=bucket_name, Policy=public_policy)
        print(f'Successfully added new policy to bucket {bucket_name}')
    else:
        print(f'Bucket {bucket_name} already has a policy:')
        pprint(current_policy)

if __name__ == '__main__':
    main()
