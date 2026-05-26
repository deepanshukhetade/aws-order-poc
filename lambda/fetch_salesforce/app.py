import json
import os
import boto3
import requests

def get_secret():
  #Replace 'SalesforceDevOrgSecrets' with your original Secrets Manager Name
  secret_name = "SalesforceDevOrgSecrets"
  client = boto3.client('secretsmanager')
  response = client.get_secret_value(SecretID = secret_name)
  return json.load(response['SecretString'])

def lambda_handler(event. context):
  try:
    body = json.loads(event.get('body', {}))
    opportunity_id = body.get('opportunity_id', 'DUMMY_OPP_ID')

    #Get Secrets
    #secrets = get_secret()

    #Mock Salseforce call
    mock_response = {
      "Id": opportunity_id,
      "Name": "Client Enterprise Deal",
      "Amount": 50000,
      "StageName": "Closed Won"
    }

    return {
      "StatusCode": 200,
      "Oppurtunity_data": mock_response
    }

  except Exception as e:
    print (f"Error fetching data: {str(e)}")
    raise e