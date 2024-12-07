import boto3
import csv
import os
import json
import logging

#configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Clients

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

#environment Variables
DYNAMO_TABLE = os.getenv('DYNAMO_TABLE', 'Performances')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC')

def lambda_handler(event, context):
    #log the entire event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    

    #catch - try block
    try:
        # Get the uploaded file details from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Log file details
        logger.info(f"Processing file: s3://{bucket}/{key}")
        
        # Download the file
        local_path = '/tmp/temp.csv'
        s3.download_file(bucket, key, local_path)
        
        # Parse the file and write to DynamoDB
        table = dynamodb.Table(DYNAMO_TABLE)
        with open(local_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Log each row for debugging
                logger.info(f"Processing row: {row}")
                
                table.put_item(Item={
                    'stage': row['Stage'],
                    'date#start': f"{row['Date']}#{row['Start']}",
                    'performer': row['Performer'],
                    'end': row['End']
                })
        
        # Send success notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="CSV Processing Successful",
            Message=f"File {key} was successfully processed and data was uploaded to DynamoDB."
        )
        return {"statusCode": 200, "body": "Success"}
    



    except Exception as e:
        # Log the full error
        logger.error(f"Error processing event: {str(e)}")
        
        # Send failure notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,


            Subject="CSV Processing Failed",
            Message=str(e)
        )
        return {"statusCode": 500, "body": str(e)}