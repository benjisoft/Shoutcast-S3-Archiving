import dotenv
import requests
import os
import boto3
import datetime
import logging
from logdna import LogDNAHandler
from botocore.exceptions import NoCredentialsError
dotenv.load_dotenv()

key = os.environ.get('log_key')
log = logging.getLogger('logdna')
log.setLevel(logging.INFO)

options = {
  'hostname': 'archive'
}

test = LogDNAHandler(key, options)

log.addHandler(test)

log.warning("Script Restarted")

ACCESS_KEY = os.environ.get('access_key')
SECRET_KEY = os.environ.get('secret_key')
stream_url = 'https://utcr.radioca.st/stream'
file_name=str(datetime.datetime.now())+'.mp3'


def uploadToAWS(local_file, bucket, s3_file):
    log.info("Uploading")
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        log.info("Upload Successful")
        os.remove(local_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        log.warning("File not found error")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        log.warning("Credential Error")
        return False

def record(file_name, i, stream_url):
    while 1==1:
        r = requests.get(stream_url, stream=True)
        while 1==1: 
            f = open(file_name,'wb')
            for block in r.iter_content(1024):
                f.write(block)
                log.info("Block Written")
                if int(os.path.getsize(file_name)) > 1049000000:
                    log.info("Block Finished")
                    i += 1
                    f.close()
                    uploadToAWS(file_name, 'utcrlive-backup', file_name)
                    r.close()

                    r = requests.get(stream_url, stream=True)
                    file_name=str(datetime.datetime.now())+".mp3"
                    f = open(file_name,'wb')

try: 
    record(file_name, 0, stream_url)
except: 
    print("Error:", arg)
    log.error("ERROR", arg)