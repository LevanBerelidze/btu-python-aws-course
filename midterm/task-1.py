import boto3

def main():
    s3 = boto3.resource('s3')

    all_buckets = s3.buckets.all()
    for bucket in all_buckets:
        if bucket.name.startswith('users'):
            print(bucket.name)

if __name__ == '__main__':
    main()