import argparse
import logging

import boto3
from botocore.exceptions import ClientError


def upload_file(file_name: str, bucket: str, object_name: str = None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--environment',
                        help='CloudReactor deployment environment')

    args = parser.parse_args()

    deployment_environment = args.environment

    bucket_suffix = ''
    file_suffix = ''
    if deployment_environment and (deployment_environment != 'production'):
        bucket_suffix = "-" + deployment_environment
        file_suffix = "." + deployment_environment

    bucket_name = 'cloudreactor-customer-setup' + bucket_suffix

    print(f"Uploading to bucket '{bucket_name}' ...")

    upload_file(f"cloudreactor-aws-role-template{file_suffix}.json", bucket_name)
    upload_file('cloudreactor-aws-deploy-role-template.json', bucket_name)

    print(f"Done uploading to bucket '{bucket_name}'.")
