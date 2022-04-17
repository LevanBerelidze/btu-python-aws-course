import boto3
import os

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-a', '--action', choices=['download', 'delete'], required=True)
    parser.add_argument('-d', '--destination', type=str, required=False, default='./')
    args = parser.parse_args()
    return args

def download_file(s3, bucket, file, destination):
    full_path = os.path.join(destination, file)
    s3.download_file(bucket, file, full_path)

def delete_file(s3, bucket, file):
    s3.delete_object(Bucket=bucket, Key=file)

def main():
    args = parse_args()
    s3 = boto3.client('s3')

    if args.action == 'download':
        print(f'Downloading file "{args.file}" to "{args.destination}"...')
        download_file(s3, args.bucket, args.file, args.destination)
        print(f'Downloaded file "{args.file}" to "{args.destination}"...')
    elif args.action == 'delete':
        print(f'Deleting file "{args.file}"...')
        delete_file(s3, args.bucket, args.file)
        print(f'Deleted file "{args.file}"...')

if __name__ == '__main__':
    main()