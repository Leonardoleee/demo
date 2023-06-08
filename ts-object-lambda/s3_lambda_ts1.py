import json
import boto3
import os
import mysql.connector

def lambda_handler(event, context):
    # TODO implement
    print(event["Records"][0]["s3"])


    s3 = boto3.resource('s3')
    #获取源s3 bucket名称
    bucketNM = event["Records"][0]["s3"]["bucket"]["name"]
    #创建源s3 bucket对应的对象变量
    bucket = s3.Bucket(bucketNM)

    message_to_send = "New objects:" + "\n" + " "

    obj_path = []

    i = 0
    breaknum = 3
    for obj in bucket.objects.all():
        #把所有的对象key组成一个字符串，做为邮件通知的内容
        message_to_send =  message_to_send + " " + obj.key
        # 获取对象url
        obj_url = "https://" + bucketNM + ".s3.me-central-1.amazonaws.com/" + obj.key
        #把源s3 bucket中的所有对象的key组装成一个待删除列表
        obj_path.append(obj_url)
        i = i + 1
        breaknum = breaknum - 1
        if breaknum == 0:
            message_to_send =  message_to_send + "\n" + " "

    print(obj_path)



    mycursor = mydb.cursor()

    for url in obj_path:
        sql = "INSERT INTO s3_bucket_obj (s3url) VALUES (%s);"
        mycursor.execute(sql, (url,))

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


    mail_subject = "There are "+ str(i) + " new objects uploaded in s3"

    print(mail_subject)
    print(message_to_send)

    sns = boto3.client('sns')
    #利用sns发送邮件通知用户
    response_sns = sns.publish(
        #从lambda函数的环境变量中获取上面创建的SNS topic的arn
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=message_to_send,
        Subject=mail_subject
    )
    return response_sns