import boto3
import os

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-d', '--destination', type=str, required=False, default='./')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    s3 = boto3.client('s3')
    files = s3.list_objects(Bucket=args.bucket)['Contents']
    print(files)

    for file in files:
        file_name = file["Key"]
        full_path = os.path.join(args.destination, file_name)
        print(full_path)
        s3.download_file(args.bucket, file_name, full_path)
        print(f'Successfully downloaded file {file_name}')

if __name__ == '__main__':
    main()
