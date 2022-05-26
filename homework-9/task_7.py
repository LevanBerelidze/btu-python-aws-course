import boto3
from argparse import ArgumentParser

from task_1 import create_vpc
from task_3 import create_internet_gateway, attach_igw_to_vpc
from task_2 import create_subnet
from task_4 import create_routing_table
from task_5 import add_route_to_internet_gateway
from task_6 import associate_route_table_with_subnet

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_cidr_block', type=str, required=True)
    parser.add_argument('-p', '--public_subnet_cidr_block', type=str, required=True)
    parser.add_argument('-s', '--private_subnet_cidr_block', type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')

    # Create VPC
    vpc_id = create_vpc(ec2_client, args.vpc_cidr_block)
    igw_id = create_internet_gateway(ec2_client)
    attach_igw_to_vpc(ec2_client, vpc_id, igw_id)

    # Create public subnet
    public_subnet_id = create_subnet(ec2_client, vpc_id, args.public_subnet_cidr_block)
    public_rtb_id = create_routing_table(ec2_client, vpc_id)
    add_route_to_internet_gateway(ec2_client, public_rtb_id, igw_id)
    associate_route_table_with_subnet(ec2_client, public_rtb_id, public_subnet_id)

    # Create private subnet
    private_subnet_id = create_subnet(ec2_client, vpc_id, args.private_subnet_cidr_block)
    private_rtb_id = create_routing_table(ec2_client, vpc_id)
    associate_route_table_with_subnet(ec2_client, private_rtb_id, private_subnet_id)


if __name__ == '__main__':
    main()