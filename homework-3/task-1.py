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
    if not os.path.exists(args.file):
        print(f'The file with path "{args.file}" not found')
        return

    if not os.path.isfile(args.file):
        print(f'The path "{args.file}" is not a file')
        return

    print(f'Uploading file "{args.file}" to bucket "{args.bucket}"...')

    s3 = boto3.client('s3')
    object_name = os.path.basename(args.file)
    
    try:
        s3.upload_file(args.file, args.bucket, object_name)
        print(f'Successfully uploaded file "{args.file}" to bucket "{args.bucket}"')
    except Exception as ex:
        print(f'Error while uploading file: ', ex)

if __name__ == '__main__':
    main()