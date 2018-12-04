from __future__ import print_function # Python 2/3 compatibility
import boto3

from boto3.dynamodb.conditions import Key

# from flask import render_template, url_for, redirect, request
from app import webapp
from app.getUuid import g_uid
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

tableName = 'hrmanage4'

def create_table():
    try:
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'candidateID',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'positionID',
                    'KeyType': 'RANGE'  #Sort key
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "candidate",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'candidateID'
                        },
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'positionID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['candidateEmail', 'skills', 'resume','candidatePhone']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "position",#query the candidate of a position
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'positionID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['candidateEmail', 'skills', 'resume','candidatePhone','candidateID']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "resumeAddr",  # query the candidate of a position
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'candidateID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['resume']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'candidateID',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'candidateName',
                #     'AttributeType': 'S'
                # },
                {
                    'AttributeName': 'positionID',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'positionName',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'managerID',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'ManagerName',
                #     'AttributeType': 'S'
                # }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except Exception as e:
        print(e)



# @webapp.route('/delete_table')

def putCandidateItem(managerID, positionID, candidateID,
            candidateEmail, candidatePhone, skills, resume):
    try:
        table = dynamodb.Table(tableName)

        response = table.put_item(
           Item={
                'managerID': managerID,
                'positionID': positionID,
                'candidateID': candidateID,

                'candidateEmail': candidateEmail,
                'candidatePhone':candidatePhone,
                'skills':skills,
                'resume':resume
            }
        )
    except Exception as e:
        print("put failed")
        print(e)
    return


#need to provide the candidateid and the positionid
#used to see the position of the pdf file
def query_candidate(candidateId, positionId):
    table = dynamodb.Table(tableName)

    cid = candidateId
    pid = positionId
    response = table.query(
        IndexName = 'candidate',
        KeyConditionExpression= Key('candidateID').eq(cid) & Key('positionID').eq(pid)
    )

    records = []
    for i in response['Items']:
        records.append(i)
    #print(records)
    return records

#query all the candidate of a position
def query_candidate_of_position(positionId):
    table = dynamodb.Table(tableName)

    pid = positionId
    response = table.query(
        IndexName = 'position',
        KeyConditionExpression= Key('positionID').eq(pid)
    )

    records = []
    for i in response['Items']:
        records.append(i)
    #print(records)
    return records

def query_resume(candidateid):
    table = dynamodb.Table(tableName)

    cid = candidateid
    response = table.query(
        IndexName='resumeAddr',
        KeyConditionExpression=Key('candidateID').eq(cid)
    )

    records = []
    for i in response['Items']:
        records.append(i)
    # print(records)
    return records

# create_table()
# x = g_uid()
#skills = {"python":"4","java":"3","machine learning":"5",'php':"0"}
#skills1 = {"python":"2","java":"0","machine learning":"5",'php':"0"}
# skills2 = {"python":"1","java":"2","machine learning":"0",'php':"2"}
# putCandidateItem(x,'7','23','Tom@google.com','778234012',skills2,'https://s3.amazonaws.com/a3-resume/lecture2_ewADCWQ.pdf')
# # # #
# # records = query_candidate_of_position('be9aa298-f2c2-11e8-a4d7-f40f242190e7')
# records = query_resume('23')
# print(records)


# skills = {"Python": {"N": 2}, "java": {"N": 2}}