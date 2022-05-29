import boto3
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-db', '--db_instance_id', type=str, required=True)
    parser.add_argument('-p', '--percentage_to_increase_by', type=str, required=False, default='25')
    return parser.parse_args()

def get_allocated_storage(rds_client, db_instance_id):
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    db_instance = response.get('DBInstances')[0]
    return db_instance.get('AllocatedStorage')

def calculate_new_storage(current_storage, percentage_to_increase_by):
    new_storage = current_storage + current_storage * percentage_to_increase_by / 100
    return int(new_storage)

def main():
    args = parse_args()
    rds_client = boto3.client('rds')
    
    current_storage = get_allocated_storage(rds_client, args.db_instance_id)
    new_storage = calculate_new_storage(current_storage, int(args.percentage_to_increase_by))
    print(f'Increasing storage of RDS instance {args.db_instance_id} from {current_storage} GiB to {new_storage} GiB...')

    rds_client.modify_db_instance(DBInstanceIdentifier=args.db_instance_id, AllocatedStorage=new_storage)
    print('Done')

if __name__ == '__main__':
    main()
