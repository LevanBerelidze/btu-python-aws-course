import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--route_table_id', type=str, required=True)
    parser.add_argument('-i', '--igw_id', type=str, required=True)
    return parser.parse_args()

def add_route_to_internet_gateway(ec2_client, route_table_id, igw_id):
    ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=route_table_id,
    )

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    add_route_to_internet_gateway(ec2_client, args.route_table_id, args.igw_id)

if __name__ == '__main__':
    main()