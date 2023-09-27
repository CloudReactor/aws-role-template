import os
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError

MAX_BODY_SIZE = 1000000


def handler(event, context):
    request_url = event['request_url']
    parsed = urlparse(request_url)

    original_request_headers = event.get('request_headers', {})

    access_key = original_request_headers.pop('X-Url-Requester-Access-Key')

    if access_key != os.environ['URL_REQUESTER_ACCESS_KEY']:
        print("Invalid access key")
        return {
            'statusCode': 401,
            'body': 'Invalid access key'
        }

    hostname = parsed.hostname
    domain_suffix = os.environ.get('DOMAIN_SUFFIX', '.cloudreactor.io')

    if (not domain_suffix.startswith('.') and (hostname != domain_suffix)) or \
        (not hostname.endswith(domain_suffix)):
        print(f"Invalid hostname: '{hostname=}'")
        return {
            'statusCode': 400,
            'body': 'Invalid hostname'
        }

    request_method = event.get('request_method', 'GET')
    request_body = event.get('request_body', None)

    request_headers = {
        'User-Agent': 'AWS Lambda',
        'Accept': 'application/json'
    }

    if request_body:
        request_headers['Content-Type'] = 'application/json'

    request_headers.update(original_request_headers)

    print(f"Executing {request_method} to {request_url} ...")

    try:
        if request_body:
            data = request_body.encode('utf-8')
        else:
            data = event.get('query')

        resp = urlopen(Request(request_url, data=data, headers=request_headers,
                               method=request_method))
        print('Request succeeded')
        # For now, no need to read response body or headers,
        # since this is executed by Cloudwatch.
        return {
            'statusCode': resp.status,
            'body': ''
        }
    except HTTPError as http_error:
        status = http_error.code
        resp_body = None
        try:
            resp_body = str(http_error.read(MAX_BODY_SIZE))
        except IOError:
            print("Can't read response body")

        print(f"Failed with status {status} with body '{resp_body}'")
        raise
