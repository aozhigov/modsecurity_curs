#!/usr/bin/env python3
import sys

import pandas as pd

splitValue = '''



'''


class Request:
    def __init__(self):
        self.headers = {}
        self.content = ''
        self.method = ''
        self.path = ''
        self.protocol = ''

    def get_maps(self):
        result = self.headers.copy()
        result['Content'] = self.content
        result['Method'] = self.method
        result['Path'] = self.path
        result['Protocol'] = self.protocol
        return result


def normalization_headers(requests, headers):
    for request in requests:
        for header in headers:
            if header not in request.headers.keys():
                request.headers[header] = None
    return requests


def checks_count_headers(requests, count):
    for request in requests:
        assert len(request.headers.keys()) == count


def create_dataframe(requests):
    data = [x.get_maps() for x in requests]
    return pd.DataFrame(data)


def parse_log(file_in):
    result = []
    headers = set()
    with open(file_in, 'r') as f:
        requests = f.read().split(splitValue)
        for request in requests:
            request_obj = parse_http(headers, request)
            result.append(request_obj)
    return result, headers


def parse_http(headers, request_str):
    request_obj = Request()
    is_content = False
    if request_str.startswith('\n'):
        request_str = request_str[1:]
    for line in request_str.split('\n'):
        if line == '':
            is_content = True
            continue
        if is_content:
            request_obj.content = line
            continue
        if '"GET' in line or '"POST' in line or '"OPTIONS' in line or '"UPDATE' in line or '"GETOPTIONS' in line\
                or '"GETHEAD' in line or '"HEAD' in line:
            request_obj.method, request_obj.path, request_obj.protocol = line.split(' ', maxsplit=2)
            request_obj.method = request_obj.method[1:]
            request_obj.protocol = request_obj.protocol[:len(request_obj.protocol) - 1]
            continue
        elif 'GET' in line or 'POST' in line or 'OPTIONS' in line or 'UPDATE' in line or 'GETOPTIONS' in line\
                or 'GETHEAD' in line or 'HEAD' in line:
            request_obj.method, request_obj.path, request_obj.protocol = line.split(' ', maxsplit=2)
            continue
        if ': ' not in line:
            request_obj.content = line
            continue

        header, value = line.split(':', maxsplit=1)
        request_obj.headers[header] = value
        headers.add(header)
    return request_obj


def main(file_in, file_out):
    requests = normalization_headers(*parse_log(file_in))
    df = create_dataframe(requests)
    df.to_csv(file_out, index=False)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
