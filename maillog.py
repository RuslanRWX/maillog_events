#!/usr/bin/python

import ConfigParser
import time
import subprocess
import select
import xml.etree.ElementTree as ET
import re

global Mail_log_file
global Sleep_tile
global Pattern_file

Conf_file = "/home/ruslan/ruslan/BUILD/maillog/maillog.conf"
config = ConfigParser.ConfigParser()
config.read(Conf_file)
Mail_log_file = config.get('main', 'mail_log_file')
Sleep_tile = int(config.get('main', 'sleep_time'))
Pattern_file = config.get('main','pattern_file')


def find_pattern(Log_data):
    tree = ET.parse(Pattern_file)
    root = tree.getroot()
    for data in root:
        number=data[0].text
        name=data[1].text
        pattern=data[2].text
        #print "Search: "+pattern+" Data: "+Log_data
        string = re.search(pattern, Log_data)
        #string = re.match(pattern, "invalid mailbox Data")
        if string:
            email=re.search(r'[\w\.-]+@[\w\.-]+', Log_data)
            print email

#    print number+" "+name+" "+pattern



def main():
    f = subprocess.Popen(['tail','-F',Mail_log_file],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)
    while True:
        if p.poll(1):
            find_pattern(f.stdout.readline())
            #print f.stdout.readline()
	    time.sleep(Sleep_tile)

if __name__ == '__main__':
    main()