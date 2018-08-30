#!/bin/bash


mkdir /etc/maillog/
cp maillog.conf /etc/maillog/
cp pattern.xml /etc/maillog/
cp maillog.py /usr/sbin/


cp maillog.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable maillog.service

echo "Please, yuo have to configure /etc/maillog/maillog.conf"
echo "to run:  systemctl start maillog.service"


