import boto3
import os

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    s3 = boto3.client('s3')

    s3.create_bucket(Bucket=args.bucket)
    print(f'Successfully created bucket "{args.bucket}"')

    object_name = os.path.basename(args.file)
    s3.upload_file(args.file, args.bucket, object_name)
    print(f'Successfully uploaded file "{args.file}" to bucket "{args.bucket}"')

if __name__ == '__main__':
    main()