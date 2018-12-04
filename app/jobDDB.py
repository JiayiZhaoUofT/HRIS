from __future__ import print_function # Python 2/3 compatibility
import boto3

from boto3.dynamodb.conditions import Key

# from flask import render_template, url_for, redirect, request
from app import webapp
from app.getUuid import g_uid
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

tableName = 'job'


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
                        'NonKeyAttributes': ['jobTitle','skills']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "skills",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'positionID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['skills']
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


def putJobItem(managerID, positionID, jobTitle, skills):
    try:
        table = dynamodb.Table(tableName)

        response = table.put_item(
           Item={
                'managerID': managerID,
                'positionID': positionID,
                'jobTitle':jobTitle,
                'skills':skills
            }
        )
    except Exception as e:
        print("put failed")
        # print(e)
        return e
    return "put job success"

#managerID -> all the jobs create by the manager
# return all the jobs created by one manager
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
    #print(records)
    return records

#positionID -> skill requierment
# return the skill set of a job
def query_skills(positionID):
    table = dynamodb.Table(tableName)

    pid = positionID
    response = table.query(
        IndexName = 'skills',
        KeyConditionExpression= Key('positionID').eq(pid)
    )

    records = []
    for i in response['Items']:
        records.append(i)
    # print(records[0]['skills'])
    return records


#create_table()
#x = g_uid()

#putJobItem(x, g_uid(),"junior java developer","java, web develop, MySQL")
#putJobItem(x, g_uid(),"math tutor","math, English")
#putJobItem(x, g_uid(),"Web developer","React, Angular, Html, CSS")
# records = query_jobs(str(x))
# print(records)
#records = query_jobs('031f0406-f2c1-11e8-a7ce-f40f242190e7')
#x = '43601e88-f2ab-11e8-ba53-f40f242190e7'
#putJobItem(x, g_uid(),"senior java developer","java, Agile, MySQL")
#records = query_skills("4220f558-f337-11e8-b8de-f40f242190e7")
#records = query_jobs("43601e88-f2ab-11e8-ba53-f40f242190e7")
#print(records)