import boto3
import botocore
import os

bucketName = "a3-resume"
s3_location = "https://s3.amazonaws.com/a3-resume/"

# aws_config_arg = {
#     'aws_access_key_id': os.environ['aws_access_key_id'],
#     'aws_secret_access_key': os.environ['aws_secret_access_key']
# }
# def s3_upload(filepath, bucketname, filename, acl = "public-read"):
#     # print(os.environ['aws_access_key_id'])
#     try:
#         s3 = boto3.client('s3')
#         # s3 = boto3.client('s3', **aws_config_arg)
#         s3.upload_file(filepath,
#                        bucketname,
#                        filename,
#                        ExtraArgs = {
#                            "ACL": acl
#                        }
#         )
#     except Exception as e:
#         print("Something Happened: ", e)
#         # return e
#     return "{}{}".format(s3_location, filename)



def s3_upload(bucketname, data, filename):
    try:
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucketname,
                      Body=data,
                      Key=filename,
                      ACL = "public-read-write",
                      ContentType = "application/pdf"
                      # ExtraArgs={
                      #     "ACL": "public-read-write"
                      # }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return "not found"
    return "{}{}".format(s3_location, filename)

def s3_download(bucketname,keyname,outPutName):
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(bucketname).download_file(keyname, outPutName)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
