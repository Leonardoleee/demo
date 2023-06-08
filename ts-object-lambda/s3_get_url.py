def lambda_handler(event, context):
    # TODO implement
    import boto3

    s3 = boto3.client('s3')
    data = s3.get_object(Bucket='winggo-test-2', Key='a.txt')
    contents = data['Body'].read()
    print(contents)