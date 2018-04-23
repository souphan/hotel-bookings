import json
import os
import time
import uuid
import boto3
dynamodb = boto3.resource('dynamodb')

## Update overbooking limits
def update(event, context):
    ## Grab the event data given by the user
    data = json.loads(event['body'])

    ## Creating a table inside DynamoDB
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the item to the database
    response = table.update_item(
        Key={
            'id': data['id']
        },
        UpdateExpression="set numberOfRooms=:p, numberOverBooking=:a",
        ExpressionAttributeValues={
            ':p': data['numberOfRooms'],
            ':a': data['numberOverBooking']
        },
        ReturnValues="UPDATED_NEW"
    )

    print("UpdateItem succeeded:")

    return response