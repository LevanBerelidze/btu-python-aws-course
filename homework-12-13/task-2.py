import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-db', '--db_instance_id', type=str, required=True)
    parser.add_argument('-s', '--snapshot_id', type=str, required=False, default='snapshot01')
    return parser.parse_args()

def create_snapshot(rds_client, db_instance_id, snapshot_id):
    rds_client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=db_instance_id,
    )

def main():
    args = parse_args()
    rds_client = boto3.client('rds')
    create_snapshot(rds_client, args.db_instance_id, args.snapshot_id)

if __name__ == '__main__':
    main()
