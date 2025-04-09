import argparse
import os

from dotenv import load_dotenv

from src.utils import auth_aws, read_file_s3, write_file_s3

parser = argparse.ArgumentParser(description="Accessing S3 buckets to read and write files in it for D2P project")
parser.add_argument("-b","--bucket_name", required=True, type=str, help="Name of the bucket in which the object is being uploaded") #required
parser.add_argument("-o","--object_name", required=True, type=str, help="Name of the object to be uploaded") #optional

# load credentials
load_dotenv('.env')

#Connecting to AWS Servers
client = auth_aws(aws_access_key=os.getenv("access_key"), 
                  aws_secret_key=os.getenv("secret_key"), 
                  region=None)

#Upload a file to specified s3 bucket and giving it a object name
write_file_s3(s3_client=client, file="data/inventory_data.csv", 
              bucket="d2p.testing.bucket", 
              object_name="inventory_data.csv")

#Read the data of the specified file in a particular bucket
df = read_file_s3(s3_client=client, 
                  bucket="d2p.testing.bucket", 
                  object_name="inventory_data.csv")