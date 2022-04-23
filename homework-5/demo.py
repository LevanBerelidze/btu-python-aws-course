import boto3
import os
import time
from tempfile import TemporaryDirectory
from argparse import ArgumentParser

TRY_COUNT = 4
WAIT_TIME_SECONDS = 5

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    file_name = os.path.basename(args.file)

    s3 = boto3.client('s3')
    s3.upload_file(args.file, args.bucket, file_name)
    print(f'Uploaded file to the bucket')

    json_file_name = f'{os.path.splitext(file_name)[0]}.json'
    with TemporaryDirectory() as temp_dir:
        for _ in range(TRY_COUNT):
            print('Waiting for JSON file upload...')
            time.sleep(WAIT_TIME_SECONDS)

            if try_download_result(s3, args.bucket, json_file_name, temp_dir):
                break

    print('Done')

def try_download_result(s3, bucket_name, file_name, dest_dir):
    temp_file_path = os.path.join(dest_dir, file_name)
    
    try:
        s3.download_file(bucket_name, file_name, temp_file_path)
    except Exception as ex:
        return False

    print(f'Downloaded JSON file. Reading its content...')

    with open(temp_file_path, 'r') as json_file:
        print('Result:')
        print(json_file.read())

    return True

if __name__ == '__main__':
    main()