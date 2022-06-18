import boto3
from argparse import ArgumentParser

KEY_PAIR_NAME = 'final-exam-ec2s'
IMAGE_ID = 'ami-09d56f8956ab235b3'

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_id', type=str, required=True)
    parser.add_argument('-s', '--subnet_id', type=str, required=True)
    parser.add_argument('-g', '--sec_group_name', type=str, required=False, default='sec-group-01')
    parser.add_argument('-p', '--key_pair_path', type=str, required=False, default='.')
    return parser.parse_args()

def create_security_group(ec2_client, vpc_id, name):
    response = ec2_client.create_security_group(
        Description=f'Security Group for VPC {vpc_id}',
        GroupName=name,
        VpcId=vpc_id
    )
    return response.get('GroupId')

def add_inbound_rule(ec2_client, sec_group_id, ip_address, port):
    ec2_client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=port,
        GroupId=sec_group_id,
        IpProtocol='tcp',
        ToPort=port,
    )

def add_inbound_rules(ec2_client, sec_group_id):
    for port in [22, 80]:
        add_inbound_rule(ec2_client, sec_group_id, '0.0.0.0/0', port)

def create_key_pair(ec2_client, key_name, parent_directory_path):
    response = ec2_client.create_key_pair(KeyName=key_name, KeyType='rsa')

    file_path = f'{parent_directory_path}/{key_name}.pem'
    with open(file_path, 'w') as file:
        file.write(response.get('KeyMaterial'))

    return response.get('KeyPairId')

def create_instance(ec2_client, key_pair_name, image_id, sec_group_id, subnet_id, volume_size_in_gb):
    ec2_client.run_instances(
        KeyName=key_pair_name,
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        ImageId=image_id,
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sdh',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': volume_size_in_gb,
                    'VolumeType': 'gp2',
                    'Encrypted': False
                },
            },
        ],
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'Groups': [sec_group_id],
                'DeviceIndex': 0,
                'SubnetId': subnet_id,
            },
        ],
        InstanceInitiatedShutdownBehavior='stop',
    )

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')

    sec_group_id = create_security_group(ec2_client, args.vpc_id, args.sec_group_name)
    print('Created security group...')

    add_inbound_rules(ec2_client, sec_group_id)
    print('Added inbound rules...')

    create_key_pair(ec2_client, KEY_PAIR_NAME, args.key_pair_path)
    print('Created key pair...')

    for volume_size_in_gb in [10, 40]:
        create_instance(ec2_client, KEY_PAIR_NAME, IMAGE_ID, sec_group_id, args.subnet_id, volume_size_in_gb)
        print(f'Launched EC2 instance with {volume_size_in_gb}GB volume...')

    print('Done')

if __name__ == '__main__':
    main()