import boto3
from argparse import ArgumentParser

DEFAULT_MYSQL_PORT = 3306
DB_USERNAME = 'db_admin'
DB_PASSWORD = 'pa$$w0rd'

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--vpc_id', type=str, required=True)
    parser.add_argument('-g', '--sec_group_name', type=str, required=False, default='sec-group-01')
    parser.add_argument('-d', '--db_instance_identifier', type=str, required=False, default='db01')
    return parser.parse_args()

def create_security_group(ec2_client, vpc_id, name):
    response = ec2_client.create_security_group(
        Description=f'Security Group for {vpc_id}',
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

def create_rds_instance(rds_client, db_instance_identifier, security_group_id):
    response = rds_client.create_db_instance(
        DBName=db_instance_identifier,
        DBInstanceIdentifier=db_instance_identifier,
        AllocatedStorage=60,
        DBInstanceClass='db.t4g.micro',
        Engine='mysql',
        MasterUsername=DB_USERNAME,
        MasterUserPassword=DB_PASSWORD,
        VpcSecurityGroupIds=[security_group_id],
        BackupRetentionPeriod=7,
        Port=DEFAULT_MYSQL_PORT,
        MultiAZ=False,
        EngineVersion='8.0',
        AutoMinorVersionUpgrade=True,
        PubliclyAccessible=True,
        StorageType='gp2',
        EnablePerformanceInsights=False,
        DeletionProtection=False,
    )
    return response.get('DBInstance').get('DBInstanceIdentifier')

def main():
    args = parse_args()
    ec2_client = boto3.client('ec2')
    rds_client = boto3.client('rds')

    sec_group_id = create_security_group(ec2_client, args.vpc_id, args.sec_group_name)
    print('Created security group...')

    add_inbound_rule(ec2_client, sec_group_id, '0.0.0.0/0', DEFAULT_MYSQL_PORT)
    print('Added inbound rule...')

    create_rds_instance(rds_client, args.db_instance_identifier, sec_group_id)
    print('Created RDS instance')

    print('done')

if __name__ == '__main__':
    main()
