import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--first_id', type=str, required=True)
    parser.add_argument('-s', '--second_id', type=str, required=True)
    return parser.parse_args()

def create_route_table(ec2_client, name):
    response = ec2_client.create_route_table(VpcId='VPC_ID')
    route_table = response.get("RouteTable")
    route_table_id = route_table.get("RouteTableId")

    ec2_client.create_tags(
        Resources=[route_table_id],
        Tags=[{"Key": "Name", "Value": name}],
    )

    return route_table_id

def attach_route_table_to_subnet(ec2_client, route_table_id, subnet_id):
    ec2_client.associate_route_table(
       RouteTableId=route_table_id,
       SubnetId=subnet_id
    )

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')

    first_route_table_id = create_route_table(ec2_client, 'public-rtb-1')
    second_route_table_id = create_route_table(ec2_client, 'private-rtb-1')

    attach_route_table_to_subnet(ec2_client, first_route_table_id, args.first_id)
    attach_route_table_to_subnet(ec2_client, second_route_table_id, args.second_id)


if __name__ == '__main__':
    main()