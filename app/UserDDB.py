from __future__ import print_function # Python 2/3 compatibility
import boto3

from boto3.dynamodb.conditions import Key

# from flask import render_template, url_for, redirect, request
from app import webapp

#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

tableName = 'userInfo'

def create_table():
    try:
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'managerID',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'positionID',
                    'KeyType': 'RANGE'  #Sort key
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "positions",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'managerID'
                        },
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'positionID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['jobTitle']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'positionID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'managerID',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except Exception as e:
        print(e)


def putJobItem(managerID, positionID, jobTitle):
    try:
        table = dynamodb.Table(tableName)

        response = table.put_item(
           Item={
                'managerID': managerID,
                'positionID': positionID,
                'jobTitle':jobTitle
            }
        )
    except Exception as e:
        print("put failed")
        print(e)
    return


def query_jobs(managerID):
    table = dynamodb.Table(tableName)

    mid = managerID
    response = table.query(
        IndexName = 'positions',
        KeyConditionExpression= Key('managerID').eq(mid)
    )

    records = []
    for i in response['Items']:
        records.append(i)
    print(records)
    return records

#create_table()
x = g_uid()
putJobItem(str(x), "sajijiwe","junior java developer")
putJobItem(str(x), "sadwaere","math tutor")
putJobItem(str(x),"jjjjjj","C++ developer")
records = query_jobs(str(x))
print(records)