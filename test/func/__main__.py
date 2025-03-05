# Import libraries needed for the integration

import ibm_boto3
import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import date
import json
from ibm_botocore.client import Config, ClientError
import logging

#Configuração de Logging
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log_file = f"{date.today()}.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

print("All libraries loaded, starting the bucket transmission...")
load_dotenv(".././ibmcloud.env")

required_env_vars = ["COS_API_KEY_ID", "COS_SERVICE_CRN", "COS_ENDPOINT", "ibm_cloud_bucket_name"]
for var in required_env_vars:
        if not os.getenv(var):
                raise ValueError(f"Environment variable {var} is not defined")

# Log das variáveis de ambiente
logger.info(f"COS_ENDPOINT: {os.getenv('COS_ENDPOINT')}")
logger.info(f"ibm_cloud_bucket_name: {os.getenv('ibm_cloud_bucket_name')}")

cos_cli = ibm_boto3.client("s3",
                           ibm_api_key_id = os.getenv("COS_API_KEY_ID"),
                           ibm_service_instance_id=os.getenv("COS_SERVICE_CRN"),
                           config=Config(signature_version="oauth"),
                           endpoint_url=os.getenv("COS_ENDPOINT")
                           )

def test_connection():
        try:
                cos_cli.list_buckets()
                logger.info("Successfully connected to IBM Cloud Object Storage")
        except Exception as e:
                logger.error(f"Failed to connect to IBM Cloud Object Storage: {e}")
                raise

def convert_to_timestamp_str(date_string):
        date_object = datetime.fromisoformat(date_string)
        timestamp = date_object.timestamp()
        return_string = str(timestamp)
        result = return_string.replace(".", ",")
        logger.info(f"Converted timestamp: {result}")
        return result

# This code is a fork from Eduardo Petecof code (https://github.com/epetecof/log-webhook-setup),
# but I changed it to work on IBM Cloud.
# Followed by the dict funtions available on this link (https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-python)

def main(dict):
        logger.info(f"Received dictionary: {dict}")
        if "payload" not in dict or dict["payload"] is None:
                raise ValueError("Input dictionary must contain a valid 'payload' key")
        
        body = dict["payload"][0].copy()  # Acesse o primeiro elemento da lista

        # Verificação rigorosa dos campos obrigatórios
        required_fields = ["log_id", "request_timestamp"]
        for field in required_fields:
                if field not in body:
                        raise ValueError(f"Payload must contain '{field}'")

        # Create a S3 object key
        object_key = f"{body.get('log_id', 'unknown_log')}_{convert_to_timestamp_str(body.get('request_timestamp', datetime.now().isoformat()))}"
        logger.info(f"Body Content: {body}")
        logger.info(f"Created object key: {object_key}")

        try:
                logger.info(f"Attempting to upload JSON to COS. Bucket: {os.environ.get('ibm_cloud_bucket_name')}, Key: {object_key}.json")
                cos_cli.put_object(
                        Bucket = os.environ.get("ibm_cloud_bucket_name"),
                        Key = object_key+".json",
                        Body = (bytes(json.dumps(body).encode("UTF-8"))),
                        ContentType = "application/json",
                )
                logger.info(f"JSON uploaded successfully. Object key: {object_key}")
                print(f"JSON uploaded successfully")
                logger.info(f"Bucket name: {os.environ.get('ibm_cloud_bucket_name')}")

                # Listar objetos após o upload
                try:
                    response = cos_cli.list_objects(Bucket=os.environ.get("ibm_cloud_bucket_name"))
                    logger.info(f"Objects in bucket: {[obj['Key'] for obj in response.get('Contents', [])]}")
                except Exception as e:
                    logger.error(f"Error listing objects: {e}")

        except ClientError as ce:
                logger.error(f"Client Error: {ce}")
                logger.error(f"Error code {ce.response['Error']['Code']}")
                logger.error(f"Error message {ce.response['Error']['Message']}")
        except Exception as e:
                logger.error(f"Error when uploading the JSON file: {e}" )
                print(f"Error when uploading the JSON file: {e}" )
        return {"statusCode": 200, "body": body}

test_connection()