#!/usr/bin/python
import boto3
import ConfigParser

Conf_file = "/etc/maillog/maillog.conf"
config = ConfigParser.ConfigParser()
config.read(Conf_file)



# Create SQS client
sqs = boto3.client('sqs')

queue = config.get('main','queue_name')
url = config.get('main','endpoint_url')
queue_url = url+"/"+queue

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']

# Delete received message from queue
sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message)