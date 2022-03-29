import boto3

# create an STS client object that represents a live connection to the 
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumed_role_object=sts_client.assume_role(
    RoleArn="arn:aws:iam::982853265726:instance-profile/flaskwebrole",
    RoleSessionName="assumerolesession"
)

# From the response that contains the assumed role, get the temporary 
# credentials that can be used to make subsequent API calls
credentials=assumed_role_object['Credentials']


# Use the temporary credentials that AssumeRole returns to make a 
# connection to Amazon S3  
s3_client = boto3.client('s3', 
                      aws_access_key_id=credentials['AccessKeyId'],
                      aws_secret_access_key=credentials['SecretAccessKey'],
                      region_name="ap-southeast-1"
                      )

s3 = boto3.resource(
    service_name='s3',
    region_name='ap-southeast-1',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey']
)

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            print(item)
            contents.append(item)
    except Exception as e:
        pass

    return contents


def show_image(bucket):
    s3_client = boto3.client('s3')
    # location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
    public_urls = []
    videos_list = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            images = presigned_url.split('?')[0]
            print("[DATA] : presigned url = ", presigned_url)
            print(images)
            print(images[-3:])
            if images[-3:] == 'png':
                public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[DATA] : The contents inside show_image = ", public_urls)
    return public_urls