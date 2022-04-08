import boto3
import os

from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    parsed_args = parser.parse_args()
    bucket_name = parsed_args.bucket
    return bucket_name

def get_extension(full_name):
    name_and_extension = os.path.splitext(full_name)
    extension = name_and_extension[1]
    extension = extension[1:]
    return extension.lower()

def main():
    bucket = parse_bucket_name()

    s3 = boto3.client('s3')
    result = s3.list_objects(Bucket=bucket)

    counts = {}

    for obj in result.get('Contents', []):
        full_name = obj.get('Key')
        extension = get_extension(full_name)

        if extension in counts:
            counts[extension] += 1
        else:
            counts[extension] = 1

    for extension in counts:
        count = counts[extension]
        print(f'{extension} - {count}')
    
if __name__ == '__main__':
    main()