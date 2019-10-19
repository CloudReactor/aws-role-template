import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def handler(event, context):
    request_url = event['request_url']
    request_method = event.get('request_method', 'GET')
    request_body = event.get('request_body', None)

    request_headers = {
        'User-Agent': 'AWS Lambda',
        'Accept': 'application/json'
    }

    if request_body:
        request_headers['Content-Type'] = 'application/json'

    request_headers.update(event.get('request_headers', {}))

    print(f"Executing {request_method} to {request_url} ...")
    resp = None
    try:
        data = None
        if request_body:
            data = request_body.encode('utf-8')

        resp=urlopen(Request(request_url, data=data, headers=request_headers, method=request_method))
        print('Request succeeded')
        return resp.status
    except HTTPError as http_error:
        status = http_error.code
        resp_body = None
        try:
            resp_body = str(http_error.read(1000000))
        except:
            print("Can't read response body")

        print(f"Failed with status {status} with body '{resp_body}'")
        raise
    except:
        raise
