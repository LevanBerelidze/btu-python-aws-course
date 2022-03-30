import boto3

def main():
	s3 = boto3.resource('s3')

	for bucket in s3.buckets.all():
		print(bucket.name)

	print('=============')

	filtered_buckets = filter(lambda b: b.name.startswith('prod'), s3.buckets.all())
	for bucket in filtered_buckets:
		print(bucket.name)
	

if __name__ == '__main__':
	main()