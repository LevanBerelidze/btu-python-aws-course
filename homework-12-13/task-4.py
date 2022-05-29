import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--region_name', type=str, required=False)
    return parser.parse_args()

def main():
    args = parse_args()
    client = boto3.client('dynamodb', region_name=args.region_name)

    response = client.list_tables()
    for table_name in response['TableNames']:
        print(table_name)

if __name__ == '__main__':
    main()