import argparse
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError


def upload_file(file_name_prefix: str, bucket_prefix: str,
        version: str, deployment_environment: str, qualify_file_name: bool):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :param qualify_file_name: If true, add the deployment environment to the filename
    :return: True if file was uploaded, else False
    """
    first_dot_index = version.find('.')
    major_version = version[:first_dot_index]

    file_name = file_name_prefix
    bucket = bucket_prefix
    deployment_qualifier = ''

    if deployment_environment and (deployment_environment != 'production'):
        bucket += '-' + deployment_environment
        deployment_qualifier = '.' + deployment_environment

    if qualify_file_name:
        file_name += deployment_qualifier

    file_name += '.json'

    full_version_object_name = file_name_prefix + '-' + version \
            + deployment_qualifier + '.json'
    major_version_object_name = file_name_prefix + '-' + major_version \
            + deployment_qualifier + '.json'

    # Upload the files
    for object_name in [full_version_object_name, major_version_object_name]:
      logging.info(f"Uploading {object_name} to {bucket} ...")
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

    with open('version.txt', 'r') as f:
        version = f.read().strip()

    if not version:
        print('version.txt could not be read')
        sys.exit(-1)

    print(f"Read {version=}")

    bucket_prefix = 'cloudreactor-customer-setup'

    upload_file(f"cloudreactor-aws-role-template",
            bucket_prefix=bucket_prefix,
            deployment_environment=deployment_environment,
            version=version, qualify_file_name=True)
    upload_file(f'cloudreactor-aws-deploy-role-template',
            bucket_prefix=bucket_prefix,
            deployment_environment=deployment_environment,
            version='1.0.0', qualify_file_name=False)

    print(f"Done uploading.")