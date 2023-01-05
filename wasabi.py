import boto3
from enums.constants import CONSTANTS

def __get_s3_client():
    return boto3.client('s3',
    endpoint_url = CONSTANTS.WASABI_ENDPOINT.value,
    aws_access_key_id = CONSTANTS.WASABI_ACCESS_KEY.value,
    aws_secret_access_key = CONSTANTS.WASABI_ACCESS_SECRET.value)
    

def get_presigned_url_to_push_object(bucket_name, folder_name, file_name, url_valid_for=600):
    s3 = __get_s3_client()
    key = "{}/{}".format(folder_name, file_name)
    
    s3_response = s3.generate_presigned_post(
        Bucket=bucket_name,
        Key=key,
        ExpiresIn= url_valid_for #time to expire in seconds
    )
    return {
        "url" : s3_response['url'],
        "connection_info": s3_response['fields']
    }


def get_presigned_url_to_access_object(bucket_name, folder_name, file_name, url_valid_for=30):
    s3 = __get_s3_client()
    key = "{}/{}".format(folder_name, file_name)

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key,
            'ResponseExpires': url_valid_for
        }
    )
    return url

def delete_file_from_bucket(bucket_name, folder_name, file_name):
    s3 = __get_s3_client()
    key = "{}/{}".format(folder_name, file_name)
    s3.delete_object(Bucket=bucket_name, Key=key)
    return True

def create_folder_inside_bucket(bucket_name, folder_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=(folder_name+'/'))