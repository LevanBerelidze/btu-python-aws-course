import boto3

from tempfile import TemporaryFile
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bucket', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    return args

def latest_version(a, b):
    return max(a, b, key=lambda v: v['LastModified'])

def find_previous_version(versions):
    result = None
    for version in versions:
        if not version['IsLatest']:
            result = latest_version(result, version) if result is not None else version
    return result

def main():
    args = parse_args()

    s3 = boto3.client('s3')

    response = s3.list_object_versions(Bucket=args.bucket, Prefix=args.file)
    if not 'Versions' in response:
        print(f'File "{args.file}" not found. Exiting...')
        return

    versions = list(filter(lambda v: v['Key'] == args.file, response['Versions']))
    if len(versions) == 0:
        print(f'File "{args.file}" not found. Exiting...')
        return

    previous_version = find_previous_version(versions)
    if previous_version is None:
        print(f'Previous version of file "{args.file}" is not available. Exiting...')
        return

    previous_version_id = previous_version['VersionId']
    with TemporaryFile() as temp_file:
        s3.download_fileobj(args.bucket, args.file, temp_file, ExtraArgs={ 'VersionId': previous_version_id })
        print(f'Downloaded version "{previous_version_id}" to temporary file')

        temp_file.seek(0)
        s3.upload_fileobj(temp_file, args.bucket, args.file)
        print(f'Successfully uploaded the previous version as a new version')

if __name__ == '__main__':
    main()