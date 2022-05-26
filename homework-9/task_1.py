import boto3

VPC_CIDR_BLOCK = '10.10.0.0/16'
VPC_NAME = 'vpc-01'
VPC_CREATOR = 'lberelidze'

def create_vpc(ec2_client, cidr_block):
    response = ec2_client.create_vpc(CidrBlock=cidr_block)
    vpc = response.get('Vpc')
    return vpc.get('VpcId')

def add_tags(ec2_client, vpc_id, vpc_name, vpc_creator):
    ec2_client.create_tags(
        Resources=[vpc_id],
        Tags=[
            { 'Key': 'Name', 'Value': vpc_name },
            { 'Key': 'Creator', 'Value': vpc_creator },
        ]
    )

def main():
    ec2_client = boto3.client('ec2')
    vpc_id = create_vpc(ec2_client, VPC_CIDR_BLOCK)
    add_tags(ec2_client, vpc_id, VPC_NAME, VPC_CREATOR)
    print(f'VPC ID: {vpc_id}')

if __name__ == '__main__':
    main()