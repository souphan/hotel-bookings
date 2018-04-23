import json
import os
import time
import uuid
import boto3
import decimalencoder
import overbook_exception

dynamodb = boto3.resource('dynamodb')

## Raises an error Exception when user has overbooked
def overbook():
    raise overbook_exception.OverBookException('Sorry! Hotel is overbooked.')

## Create a hotel booking if not overbooked
def create(event, context):
    ## Grab the event data given by the user
    data = json.loads(event['body'])

    ## Timestamp created for hotel booking insertss
    timestamp = int(time.time() * 1000)

    ## Creating a table inside DynamoDB
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    ## Grab all data from the database
    resultList = table.scan()
    bookings_placed = []

    ## Loop through data dictionary and store data in variables
    for li in resultList['Items']:
        if 'email' in li:
            bookings_placed.append(li['email'])
        if 'numberOfRooms' in li:
            booking_number_rooms = li['numberOfRooms']
        if 'numberOverBooking' in li:
            ## Get percent value of overbooking
            booking_number_overbook =  (li['numberOverBooking'] * li['numberOfRooms']) / 100

    ## Get overbooking percent
    over_booking_percent = booking_number_rooms * booking_number_overbook
    ## Get overbooking amount the hotel is allowing
    overbooking_amount = over_booking_percent + booking_number_rooms

    ## Only allow booking to take place if the number of 
    ## rooms booked is less than bookings placed plus overbooking amount
    ## if over the limit, then throw error Exception
    if len(bookings_placed) <= booking_number_rooms or len(bookings_placed) <= overbooking_amount:
        ## Items to populate the table
        item = {
            'id': str(uuid.uuid1()),
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'email': data['email'],
            'arrival': data['arrival'],
            'departure': data['departure'],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        # write the item to the database
        table.put_item(Item=item)

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item),
            "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
            }
        }
    else:
        return overbook()

    return response