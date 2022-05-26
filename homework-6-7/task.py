import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_name', type=str, required=True)
    parser.add_argument('-ip', '--cidr_block', type=str, required=True)
    return parser.parse_args()

def create_vpc(ec2_client, cidr_block):
    response = ec2_client.create_vpc(CidrBlock=cidr_block)
    vpc = response.get('Vpc')
    return vpc.get('VpcId')

def set_vpc_name(ec2_client, vpc_id, vpc_name):
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{ 'Key': 'Name', 'Value': vpc_name }])

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

    vpc_id = create_vpc(ec2_client, args.cidr_block)
    set_vpc_name(ec2_client, vpc_id, args.vpc_name)

    igw_id = create_internet_gateway(ec2_client)
    attach_igw_to_vpc(ec2_client, vpc_id, igw_id)

if __name__ == '__main__':
    main()