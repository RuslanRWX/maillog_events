#!/bin/bash


mkdir /etc/maillog/
cp maillog.conf /etc/maillog/
cp pattern.xml /etc/maillog/
cp maillog.py /usr/sbin/


cp maillog.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable maillog.service


echo "to run:  systemctl start maillog.service"
