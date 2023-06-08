import json
import boto3
import mysql.connector

s3Client = boto3.client('s3')


def lambda_handler(event, context):
    #Get our bucket and file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(bucket)
    print(key)

    obj_url = "https://" + bucket + ".s3.me-central-1.amazonaws.com/" + key
    mycursor = mydb.cursor()
    sql = "INSERT INTO s3_bucket_obj (s3url) VALUES (%s);"
    mycursor.execute(sql, (obj_url,))

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

    #Get our object
    response = s3Client.get_object(Bucket=bucket, Key=key)

    #Process it
    data = response['Body'].read().decode('utf-8')
    print(data)
