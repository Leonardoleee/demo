import json
import os
import mysql.connector
obj_path = ['https://winggo-test-2.s3.me-central-1.amazonaws.com/b.txt', 'https://winggo-test-2.s3.me-central-1.amazonaws.com/b1/', 'https://winggo-test-2.s3.me-central-1.amazonaws.com/b1/c.txt', 'https://winggo-test-2.s3.me-central-1.amazonaws.com/c.txt', 'https://winggo-test-2.s3.me-central-1.amazonaws.com/finish.txt', 'https://winggo-test-2.s3.me-central-1.amazonaws.com/lambda.zip']

mydb = mysql.connector.connect(
    host="database-test-1.cppsarmc7haf.me-central-1.rds.amazonaws.com",
    user="admin",
    password="Jb3figgznN7U",
    database="s3test"
)

mycursor = mydb.cursor()

for url in obj_path:
    sql = "INSERT INTO s3_bucket_obj (s3url) VALUES (%s);"
    mycursor.execute(sql, (url,))

mydb.commit()

print(mycursor.rowcount, "record inserted.")