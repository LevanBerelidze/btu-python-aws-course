import boto3

from argparse import ArgumentParser

def parse_bucket_name():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)        
    parsed_args = parser.parse_args()
    bucket_name = parsed_args.bucket
    return bucket_name

def list_bucket_files(s3, bucket):
    response = s3.list_objects(Bucket=bucket)

    result = []
    for obj in response.get('Contents', []):
        file_name = obj.get('Key')
        result.append(file_name)
    
    return result

def main():
    bucket = parse_bucket_name()
    s3 = boto3.client('s3')
    file_names = list_bucket_files(s3, bucket)
    sorted_file_names = sorted(file_names)
    for file_name in sorted_file_names:
        print(file_name)

if __name__ == '__main__':
    main()