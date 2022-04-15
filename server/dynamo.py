import boto3
from serverconfig import aws_key, aws_secret

dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
                          aws_access_key_id=aws_key,
                          aws_secret_access_key=aws_secret)

table1 = dynamodb.Table('2PC-1')
table2 = dynamodb.Table('2PC-2')