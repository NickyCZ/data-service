import json
import boto3

def lambda_handler(event, context):
    sqs_message = json.loads(event['Records'][0]['body'])
    commodity = sqs_message['instrument']
    
    # specify the DynamoDB table to retrieve data from
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('my-dynamodb-table')
    
    response = table.get_item(Key={'id': 'instrument'})

    data = response['Item']['corn_data']
    # publish the data to an SNS topic
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:123456789012:my-sns-topic',
        Message=json.dumps({'instrument': commodity, 'data': data})
    )
