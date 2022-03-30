import boto3

def main():
	s3 = boto3.resource('s3')

	all_buckets = s3.buckets.all()
	filtered_buckets = filter(lambda b: b.name.startswith('prod'), all_buckets)

	for bucket in filtered_buckets:
		print(bucket.name)
	

if __name__ == '__main__':
	main()