import base64
import datetime
import json
import os
import logging

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


default_log_args = {
    "level": logging.DEBUG if os.environ.get("DEBUG", False) else logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M",
    "force": True,
}


logging.basicConfig(**default_log_args)
log = logging.getLogger("Basic-Authorizer-Lambda")




def lambda_handler(event, context):
    # Extract headers from the Lambda event
    headers = event.get('headers', {})

    log.info("event: %s", event)
    log.info("headers: %s", headers)


    # Check if 'Authorization' header is present
    if 'authorization' in headers:
        # Extract the value of the 'Authorization' header
        auth_header = headers['authorization']

        # Check if the header starts with 'Basic '
        if auth_header.startswith('Basic '):
            # Remove the 'Basic ' prefix and decode the base64-encoded credentials
            encoded_credentials = auth_header[6:]
            credentials = base64.b64decode(encoded_credentials).decode('utf-8')

            # Split the credentials into username and password
            username, password = credentials.split(':', 1)

            # Perform your authentication logic here
            if is_valid_credentials(username, password):
                return getAuthResponse(event, username, 'Allow')
            else:
                return getAuthResponse(event, username, 'Deny')

    # If 'Authorization' header is not present, return 401 Unauthorized
    return {
        'statusCode': 401,
        'body': 'Authorization header not found'
    }

def is_valid_credentials(username, password):
    # Implement your authentication logic here
    # For example, you might check against a database of users and passwords
    # In a real-world scenario, use a secure method for handling credentials.
    # This example uses a simple check for demonstration purposes.
    valid_username = 'genai'
    valid_password = 'capgemini!'

    return username == valid_username and password == valid_password



def getAuthResponse(event, principalId, permission):

    apiOptions = {}
    tmp =  event.get('methodArn', {}).split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]
    awsRegion = tmp[3]
    restApiId = apiGatewayArnTmp[0]
    stage = apiGatewayArnTmp[1]
    apiArn = 'arn:aws:execute-api:' + awsRegion + ':' + awsAccountId + ':' + restApiId + '/' + stage + '/*/*'

    log.info("api arn: %s", apiArn)


    auth_response = {
      "principalId": principalId, 
      "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Action": "execute-api:Invoke",
            "Effect": permission,
            "Resource": apiArn
          }
        ]
      }
    }
    
    return auth_response