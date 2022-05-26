import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_id', type=str, required=True)
    return parser.parse_args()

def create_routing_table(ec2_client, vpc_id):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get('RouteTable')
    return route_table.get('RouteTableId')

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    rtb_id = create_routing_table(ec2_client, args.vpc_id)
    print(f'Routing Table ID: {rtb_id}')

if __name__ == '__main__':
    main()