#!/usr/bin/env python3

import re
import sys

req = {}
req_names = ['GET', 'POST', 'HEAD', 'OPTIONS', 'UPDATE', ]


def get_time(string):
    arr = string.split(' ')
    arr[0] = arr[0][1:]
    l5 = len(arr[4])
    arr[4] = arr[4][:l5 - 1]
    arr[3] = arr[3][:8]
    result = ' '.join(arr)
    return result


def add_header(current_req, value):
    if value.find('\\r\\n') > -1:
        value = value[:-4]
    if len(value) == 1:
        return current_req + value
    return current_req + value + '\n'


def split_method(name, req, time):
    requests = []
    for n_req in range(len(req[time])):
        tmp = req[time][n_req].split(name)
        for i in range(len(tmp)):
            if len(tmp[i]) > 1:
                name_in_start = False
                for j in range(len(req_names)):
                    if tmp[i].find(req_names[j]) == 0:
                        name_in_start = True
                if not name_in_start:
                    tmp[i] = name + tmp[i]
                for request in tmp:
                    if len(request) > 1:
                        requests.append(request)
    return requests


def split_log(logs):
    global req
    for time in logs.keys():
        req[time] = [logs[time]]
        for name in req_names:
            req[time] = split_method(name, req, time)


def main(file_in, file_out):
    res = {}
    with open(file_in, 'r') as f:
        while True:
            tmp = f.readline()
            if not tmp:
                break
            k = re.search(r'\[.+?\]', tmp)  # find record with date and time
            k = k.group(0)
            time = get_time(k)
            idx = tmp.find('mod_dumpio.c(100)')
            if idx > -1:
                v = tmp.find('dumpio_in (data-HEAP):') + 23
                if time in res.keys():
                    res[time] = add_header(res[time], tmp[v:-1])
                else:
                    res[time] = add_header('', tmp[v:-1])
    split_log(res)
    with open(file_out, 'a') as f:
        for k in req.keys():
            for r in req[k]:
                f.write('Date-time: ' + k + '\n')
                f.write(r + '\n\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
