import boto3

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    print(f'Deleting file "{args.file}" from bucket "{args.bucket}"...')

    s3 = boto3.client('s3')
    
    try:
        s3.delete_object(Bucket=args.bucket, Key=args.file)
        print(f'Successfully deleted file "{args.file}" from bucket "{args.bucket}"')
    except Exception as ex:
        print(f'Error while deleting file: ', ex)

if __name__ == '__main__':
    main()