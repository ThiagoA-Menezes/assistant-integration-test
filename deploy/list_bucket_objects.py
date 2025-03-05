## Import libraries needed for the integration
#
#import ibm_boto3
#import os
#from dotenv import load_dotenv
#from datetime import datetime
#import json
#from ibm_botocore.client import Config, ClientError
#import logging
#

#print("All libraries loaded, starting the bucket transmission...")
#load_dotenv("./ibmcloud.env")

## This code was obtained from https://cloud.ibm.com/apidocs/cos/cos-compatibility?code=python#listobjectsv2
## the main object here is to list the objects in a bucket. The code is working fine.
## I've removed max_keys from the function signature and the call to the function.
## since its optional and I'm not using it, if you need to add it, the commands are in the lines that should be applied.
#
#def get_bucket_contents_v2(bucket_name): #, max_keys
#    print("Retrieving bucket contents from: {0}".format(bucket_name))
#    try:
#        # create client object
#        cos_cli = ibm_boto3.client("s3",
#            ibm_api_key_id=os.getenv("COS_API_KEY_ID"),
#            ibm_service_instance_id=os.getenv("COS_SERVICE_CRN"),
#            config=Config(signature_version="oauth"),
#            endpoint_url=os.getenv("COS_ENDPOINT"))
#
#        more_results = True
#        next_token = ""
#
#        while (more_results):
#            response = cos_cli.list_objects_v2(Bucket=bucket_name, ContinuationToken=next_token) #, MaxKeys=max_keys
#            files = response["Contents"]
#            for file in files:
#                print("Item: {0} ({1} bytes).".format(file["Key"], file["Size"]))
#
#            if (response["IsTruncated"]):
#                next_token = response["NextContinuationToken"]
#                print("...More results in next batch!\n")
#            else:
#                more_results = False
#                next_token = ""
#
#    except ClientError as be:
#        print("CLIENT ERROR: {0}\n".format(be))
#    except Exception as e:
#        print("Unable to retrieve bucket contents: {0}".format(e))# %%


#get_bucket_contents_v2("assistant-test")

