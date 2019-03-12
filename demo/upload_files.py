#!/usr/bin/env python3
import base64
import random
import string
import json
import requests

CMS_SERVER = '10.152.183.241'

FILES = [
    {'path': 'files/video1.mp4', 'times': 10},
    #{'content': b'test', 'times': 10},
]


def upload_file(data):
    req = dict()
    req['resourceAuthor'] = 'sastix'
    req['resourceBinary'] = data
    req['resourceMediaType'] = 'video/mp4'
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    req['resourceName'] = name + '.mp4'
    req['resourceTenantId'] = '1'

    url = 'http://{}/cms/v1.0/createResource/'.format(CMS_SERVER)
    response = json.loads(requests.post(url, json=req).text)
    return response['resourceURI']


def read_file(path):
    with open(path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string


def upload_all_files():
    urls = list()
    for file in FILES:
        if 'path' in file:
            data = read_file(file['path'])
        elif 'content' in file:
            data = file['content']
        for i in range(file['times']):
            uid = upload_file(data)
            urls.append('http://{}/cms/v1.0/getData/{}'.format(CMS_SERVER, uid))

    return urls


if __name__ == '__main__':
    urls = upload_all_files()
    with(open('urls.txt', 'w')) as f:
        for url in urls:
            f.write(url + '\n')
            print(url)
