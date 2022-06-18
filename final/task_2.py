import boto3
from argparse import ArgumentParser

VPC_CIDR_BLOCK = '10.10.0.0/16'
VPC_NAME = 'vpc-01'
VPC_CREATOR = 'lberelidze'

PUBLIC_SUBNET_NAME = 'public-subnet'
PRIVATE_SUBNET_NAME = 'private-subnet'
PUBLIC_SUBNET_CIDR_BLOCK = '10.10.1.0/24'
PRIVATE_SUBNET_CIDR_BLOCK = '10.10.2.0/24'

def create_vpc(ec2_client, cidr_block):
    response = ec2_client.create_vpc(CidrBlock=cidr_block)
    vpc = response.get('Vpc')
    return vpc.get('VpcId')

def add_tags_to_vpc(ec2_client, vpc_id, vpc_name, vpc_creator):
    ec2_client.create_tags(
        Resources=[vpc_id],
        Tags=[
            { 'Key': 'Name', 'Value': vpc_name },
            { 'Key': 'Creator', 'Value': vpc_creator },
        ]
    )

def create_subnet(ec2_client, vpc_id, cidr_block):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    subnet = response.get('Subnet')
    return subnet.get('SubnetId')

def add_name_tag_to_subnet(ec2_client, subnet_id, name):
    ec2_client.create_tags(
        Resources=[subnet_id],
        Tags=[{"Key": "Name", "Value": name}],
    )

def create_routing_table(ec2_client, vpc_id):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get('RouteTable')
    return route_table.get('RouteTableId')

def associate_route_table_with_subnet(ec2_client, route_table_id, subnet_id):
    ec2_client.associate_route_table(
       RouteTableId=route_table_id,
       SubnetId=subnet_id
    )

def main():
    ec2_client = boto3.client('ec2')

    vpc_id = create_vpc(ec2_client, VPC_CIDR_BLOCK)
    print(f'Created VPC with ID: {vpc_id}...')

    add_tags_to_vpc(ec2_client, vpc_id, VPC_NAME, VPC_CREATOR)
    print('Added tags to VPC...')

    public_subnet_id = create_subnet(ec2_client, vpc_id, PUBLIC_SUBNET_CIDR_BLOCK)
    add_name_tag_to_subnet(ec2_client, public_subnet_id, PUBLIC_SUBNET_NAME)
    public_rtb_id = create_routing_table(ec2_client, vpc_id)
    associate_route_table_with_subnet(ec2_client, public_rtb_id, public_subnet_id)
    print('Created public subnet...')

    private_subnet_id = create_subnet(ec2_client, vpc_id, PRIVATE_SUBNET_CIDR_BLOCK)
    add_name_tag_to_subnet(ec2_client, private_subnet_id, PRIVATE_SUBNET_NAME)
    private_rtb_id = create_routing_table(ec2_client, vpc_id)
    associate_route_table_with_subnet(ec2_client, private_rtb_id, private_subnet_id)
    print('Created private subnet...')

    print('Done')


if __name__ == '__main__':
    main()