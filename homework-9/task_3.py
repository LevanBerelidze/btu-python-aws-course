import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_id', type=str, required=True)
    return parser.parse_args()

def create_internet_gateway(ec2_client):
    response = ec2_client.create_internet_gateway()
    igw = response.get('InternetGateway')
    return igw.get('InternetGatewayId')

def attach_igw_to_vpc(ec2_client, vpc_id, igw_id):
    ec2_client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    igw_id = create_internet_gateway(ec2_client)
    attach_igw_to_vpc(ec2_client, args.vpc_id, igw_id)
    print(f'Internet Gateway ID: {igw_id}')

if __name__ == '__main__':
    main()