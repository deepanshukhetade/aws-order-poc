from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3
import json

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2026, 1, 1),
  'retries': 1,
  'retry_delay': timedelta(minutes=5)
}

def retry_failed_orders():
  dynamodb = boto3.resource('dynamodb', region_name = 'ap-south-1')
  table = dynamodb.Table('ProcessedOrders')
  sfn_client = boto3.client('stepfunctions', region_name = 'ap-south-1')

  #Query Dynamodb GSI for failed orders
  response = table.query(
    IndexName = 'StatusIndex',
    KeyConditionExpression = boto3.dynamodb.conditions.key('status').eq('Failed')
  )

  failed_items = response.get('Items', [])
  
  for item in failed_items:
    #Trigger failed items retry

    print(f"Retrying Order: {item['OrderId']}")
    sfn_client.start_execution(
      stateMachineArn = "stateMachine ARN" # Replace the ARN with actual one
      name = f"Retry-{item['OrderId']}"
      input = json.dumps({"opportunity_id": item.get('SalesforceId')}) 
    )

with DAG(
  'daily_failed_order_retry',
  default_args = default_args,
  schedule_ivterval = '@daily',
  catchup = False
) as dag:
  retry_task = PythonOperator(
    task_id = 'retry_failed_orders',
    python_callable = retry_failed_orders
  )