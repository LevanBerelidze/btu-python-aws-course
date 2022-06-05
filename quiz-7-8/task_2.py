import secrets
import string
import json
import boto3
from argparse import ArgumentParser

PASSWORD_LENGTH = 15
GROUP_NAME = 'Admins'
POLICY_ARN = 'arn:aws:iam::aws:policy/AdministratorAccess'
FILENAME = 'creds.json'

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-n', '--username', type=str, required=True)
    return parser.parse_args()

def generate_random_password(length=12):
   alphabet = string.ascii_letters + string.digits
   password = ''.join(secrets.choice(alphabet) for _ in range(length))
   return password

def create_user(iam_client, username, password):
   iam_client.create_user(
       UserName=username,
   )
   iam_client.create_login_profile(
       UserName=username,
       Password=password,
       PasswordResetRequired=False
   )

def create_group(iam_client, group_name):
   iam_client.create_group(GroupName=group_name)


def attach_policy_to_group(iam_client, group_name, policy_arn):
   iam_client.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)

def add_user_to_group(iam_client, username, group_name):
   iam_client.add_user_to_group(GroupName=group_name, UserName=username)

def write_credentials_to_file(username, password, filename):
    credentials = {
        'username': username,
        'password': password,
    };
    with open(FILENAME, 'w') as output_file:
        json.dump(credentials, output_file)

def main():
    args = parse_args()
    iam_client = boto3.client('iam')

    password = generate_random_password(15)
    create_user(iam_client, args.username, password)
    print('Created user...')

    create_group(iam_client, GROUP_NAME)
    print('Created group...')

    attach_policy_to_group(iam_client, GROUP_NAME, POLICY_ARN)
    print('Attached policy to group...')
    
    add_user_to_group(iam_client, args.username, GROUP_NAME)
    print('Added user to group...')

    write_credentials_to_file(args.username, password, FILENAME)
    print('Wrote credentials to file...')

    print('Done')

if __name__ == '__main__':
    main()