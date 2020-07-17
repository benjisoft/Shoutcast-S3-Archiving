import requests
import os
import boto3
import datetime
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = os.environ.get('access_key')
SECRET_KEY = os.environ.get('secret_key')
stream_url = 'https://utcr.radioca.st/stream'
i=0
file_name=str(datetime.datetime.now())+'.mp3'


def uploadToAWS(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        os.remove(local_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

while 1==1:
    r = requests.get(stream_url, stream=True)
    while 1==1: 
        f = open(file_name,'wb')
        for block in r.iter_content(1024):
            f.write(block)
            if int(os.path.getsize(file_name)) > 1049000000:
                i += 1
                f.close()
                uploadToAWS(file_name, 'utcrlive-backup', file_name)

                file_name=str(datetime.datetime.now())+".mp3"
                f = open(file_name,'wb')
