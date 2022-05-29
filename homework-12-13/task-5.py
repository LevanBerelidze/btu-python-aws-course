import os
import json
import boto3
from decimal import Decimal
from argparse import ArgumentParser

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-t', '--table_name', type=str, required=True)
    parser.add_argument('-o', '--output_directory', type=str, required=False, default='.')
    return parser.parse_args()

def main():
    args = parse_args()
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(args.table_name)
    items = table.scan()
    
    output_as_json = json.dumps(items.get('Items'), indent=4, cls=DecimalEncoder)
    output_file = os.path.join(args.output_directory, f'{args.table_name}.json')
    with open(output_file, 'w') as file:
        file.write(output_as_json)

if __name__ == '__main__':
    main()