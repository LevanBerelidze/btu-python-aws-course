import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--route_table_id', type=str, required=True)
    parser.add_argument('-n', '--subnet_id', type=str, required=True)
    return parser.parse_args()

def associate_route_table_with_subnet(ec2_client, route_table_id, subnet_id):
    ec2_client.associate_route_table(
       RouteTableId=route_table_id,
       SubnetId=subnet_id
    )

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    associate_route_table_with_subnet(ec2_client, args.route_table_id, args.subnet_id)

if __name__ == '__main__':
    main()