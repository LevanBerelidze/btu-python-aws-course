import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-v", "--vpc_id", type=str, required=True)
    parser.add_argument("-s", "--subnet_id", type=str, required=True)
    parser.add_argument("-k", "--key_pair_name", type=str, required=True)
    return parser.parse_args()

def create_security_group(ec2_client, vpc_id):
    response = ec2_client.create_security_group(
        Description="Sec Group Description",
        GroupName="Sec Group Name",
        VpcId=vpc_id)
    group_id = response.get("GroupId")
    return group_id

def add_port_access_to_sg(ec2_client, sg_id, port):
    ec2_client.authorize_security_group_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=port,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=port,
    )

def run_ec2_instance(ec2_client, subnet_id, key_pair_name, sg_id):
    ec2_client.run_instances(
        KeyName=key_pair_name,
        InstanceType="t2.micro",
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sdh",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 9,
                    "VolumeType": "gp2",
                    "Encrypted": False
                },
            },
        ],
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "Groups": [sg_id],
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
            },
        ],
    )

def main():
    args = parse_args()
    ec2_client = boto3.client("ec2")

    sg_id = create_security_group(ec2_client, args.vpc_id)
    for port in [22, 80, 443]:
        add_port_access_to_sg(ec2_client, sg_id, port)

    run_ec2_instance(ec2_client, args.subnet_id, args.key_pair_name, sg_id)

if __name__ == "__main__":
    main()