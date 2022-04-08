import boto3
import os

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-d', '--destination', type=str, required=False, default='./')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if not os.path.exists(args.destination):
        print(f'The directory with path "{args.destination}" not found')
        return

    if not os.path.isdir(args.destination):
        print(f'The path "{args.destination}" is not a directory')
        return

    print(f'Downloading file "{args.file}" from bucket "{args.bucket}" to directory "{args.destination}"')

    s3 = boto3.client('s3')

    try:
        full_path = os.path.join(args.destination, args.file)
        s3.download_file(args.bucket, args.file, full_path)
        print(f'Successfully downloaded file')
    except Exception as ex:
        print(f'Failed to download file: ', ex)

if __name__ == '__main__':
    main()