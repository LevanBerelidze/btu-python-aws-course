from argparse import ArgumentParser
from create_bucket import create_bucket
from create_lambda import create_lambda
from configure_trigger import grant_permission, add_trigger

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--function', type=str, required=True, help='The name of Lambda Function')
    parser.add_argument('-b', '--bucket', type=str, required=True, help='The unique name of S3 Bucket')
    parser.add_argument('-r', '--role', type=str, required=True, help='ARN of the role of the created Lambda Function')
    parser.add_argument('-c', '--code', type=str, required=True, help='The path to the source code that will be executed as a Lambda Function')
    parser.add_argument('-m', '--handler', type=str, required=False, default='lambda_handler', help='The name of the handler function inside the source code file')
    return parser.parse_args()

def main():
    args = parse_args()

    create_bucket(args.bucket)
    print(f'Created bucket "{args.bucket}"')

    lambda_arn = create_lambda(args.function, args.role, args.code, args.handler)
    print(f'Created lambda function "{args.function}"')

    grant_permission(lambda_arn, args.bucket)
    print(f'Granted bucket "{args.bucket}" the permission to invoke lambda function')

    add_trigger(lambda_arn, args.bucket)
    print(f'Added trigger to "{args.bucket}"')

    print('Done')

if __name__ == '__main__':
    main()