import boto3
import datetime
import json
import logging

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    client = boto3.client('eks', region_name='us-east-1')

    try:
        # Your existing code
        response = client.update_nodegroup_config(
            clusterName='genai-dev-eks-55zjxxtR',
            nodegroupName='genai-dev-eks-ng-public',
            scalingConfig={
                'minSize': 0,
                'maxSize': 1,
                'desiredSize': 0
            }
        )

        # Convert datetime object to string using custom JSON encoder
        response_json = json.dumps(response, cls=DateTimeEncoder)

        # Log the response
        logger.info("Update Nodegroup Config Response: %s", response_json)

        return response_json


    except Exception as e:
        # Log any exceptions that occur
        logger.error("An error occurred: %s", str(e))
        raise e

