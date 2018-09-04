#!/usr/bin/python
# version 0.0.1
# Copyright (c) 2018 Ruslan Variushkin,  ruslan@host4.biz

import ConfigParser
import time
import subprocess
import select
import xml.etree.ElementTree as ET
import re
import boto3
import json
import logging.handlers
import socket

Conf_file = "/etc/maillog/maillog.conf"
config = ConfigParser.ConfigParser()
config.read(Conf_file)
Mail_log_file = config.get('main', 'mail_log_file')
Sleep_tile = int(config.get('main', 'sleep_time'))
Pattern_file = config.get('main','pattern_file')
Queue =  config.get('main','queue_name')
Logs =  int(config.get('main','Logs'))
aws_access_key_id = config.get('main','aws_access_key_id')
aws_secret_access_key = config.get('main','aws_secret_access_key')
region_name = config.get('main','region_name')
hostname = socket.gethostname()


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def add_to_queue(number, name, email):
    data=json.dumps({'ID': number, 'name': name, 'email': email, 'hostname': hostname})
    sqs = boto3.resource('sqs',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name = region_name)
    queue = sqs.get_queue_by_name(QueueName=Queue)
    response = queue.send_message(MessageBody=data)
    message_id=response.get('MessageId')
    if Logs == 1:
        log_data = "ID:"+message_id +" "+data
        log.debug(log_data)
        #log.critical('this is critical')


def find_pattern(log_data):
    tree = ET.parse(Pattern_file)
    root = tree.getroot()
    for data in root:
        number=str(data[0].text)
        name=data[1].text
        pattern=data[2].text
        string = re.search(pattern, log_data)

        if string:
            emails=re.findall(r'[\w\.-]+@[\w\.-]+', log_data)
            add_to_queue(number, name, emails[1])


def main():
    f = subprocess.Popen(['tail','-F',Mail_log_file],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)
    while True:
        if p.poll(1):
            find_pattern(f.stdout.readline())
	    time.sleep(Sleep_tile)

if __name__ == '__main__':
    main()