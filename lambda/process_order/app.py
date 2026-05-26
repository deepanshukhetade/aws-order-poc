import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'ProcessedOrders'),
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
  try: 
    # Data from previous step function
    opp_data = event.get('opportunity_data', {})

    #Validation
    if opp_data.get('StageName') != 'Closed Won':
      raise ValueError('Opportunity is not closed won')
    
    #Transformation
    order_record = {
      'OrderId': f"ORD-{opp_data['Id']}",
      'salesforceId': opp_data['Id'],
      'TotalValue': opp_data['Amount'],
      'Status': 'PROCESSED',
      'ProcessedAt': datetime.utcnow().isoformat()
    }

    #Storage
    table.put_item(Item = order_record)

    return{
      "StatueCode": 200,
      "message": "Order Processed Successfully",
      "order": order_record
    }
  
  except Exception as e:
    #Log faliure for AirFlow to pick up
    failed_record = {
      'OrderId': f"FAILED-{datetime.utcnow().timestamp()}",
      'Status': 'FAILED',
      'ErrorReason': str(e)
    }
    table.put_item(Item = failed_record)
    raise e