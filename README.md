# Hotel Booking

Hotel application for booking rooms

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This application uses Serverless and AWS DynamoDB for api calls, so we need to install Serverless and configure AWS credentials.

### Installing

Clone the repo:

```
git clone https://github.com/souphan/hotel-bookings.git
```

Change directory into `hotel-bookings`:
```
cd hotel-bookings
```

Now install Serverless by running the command:

```
npm install -g serverless
```

Next you need to set up your AWS provider by following the steps here:
```
serverless config credentials --provider aws --key xxx --secret xxx
```
The keys has been provided via email.

Check Serverless info:
```
serverless info
```

You should see the following api configuration:
```
Service Information
service: hotel-management
stage: dev
region: us-east-1
stack: hotel-management-dev
api keys:
  None
endpoints:
  POST - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
  GET - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
  PUT - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
functions:
  create: hotel-management-dev-create
  list: hotel-management-dev-list
  update: hotel-management-dev-update
souphans-MBP:hotel-bookings souphan$ serverless info
Service Information
service: hotel-management
stage: dev
region: us-east-1
stack: hotel-management-dev
api keys:
  None
endpoints:
  POST - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
  GET - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
  PUT - https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking
functions:
  create: hotel-management-dev-create
  list: hotel-management-dev-list
  update: hotel-management-dev-update
```

If you don't see it, then deploy the Serverless configuration using this command:

```
serverless deploy
```

## Using the API's

Once that is done we can start testing our API's via the following `curl` commands:

First check what data we have in DynamoDB:
```
curl -X GET https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking | json_pp 
```
Expected response:
```
[
   {
      "id" : "1",
      "numberOfRooms" : 10,
      "numberOverBooking" : 2
   }
]
```

Next we can update the overbooking limit that we got back from the `GET` call by running this command:
```
curl -X PUT https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking --data '{"id":"1", "numberOfRooms":12, "numberOverBooking": 4}'
```
We can ignore the `PUT` message `Internal server error` as it doesn't affect our call, and I don't see an error in AWS Cloudwatch logs.

Check if the data has been update by the `GET` call again:
```
curl -X GET https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking | json_pp 
```

Now start booking hotels until the overbooking allowed limit is reached:
```
curl -X POST https://hdq9aqzi77.execute-api.us-east-1.amazonaws.com/dev/booking --data '{"firstName":"Roman", "lastName": “Mazur”, "email”:”roman@gmail.com", "arrival":"2018-04-21", "departure":"2018-04-29”}’
```

Do a `GET` call to check DynamoDB is being populated with new booking reservations.

Once the booking limit is reached we hit a `Exception` call that is logged in Cloudwatch.

