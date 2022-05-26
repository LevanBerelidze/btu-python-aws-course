import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_id', type=str, required=True)
    parser.add_argument('-c', '--cidr_block', type=str, required=True)
    return parser.parse_args()

def create_subnet(ec2_client, vpc_id, cidr_block):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    subnet = response.get('Subnet')
    return subnet.get('SubnetId')

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    subnet_id = create_subnet(ec2_client, args.vpc_id, args.cidr_block)
    print(f'Subnet ID: {subnet_id}')

if __name__ == '__main__':
    main()