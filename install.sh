#!/bin/bash

mkdir /etc/maillog/
cp maillog.conf /etc/maillog/
cp pattern.xml /etc/maillog/
cp maillog.py /usr/sbin/

if [ -f /etc/redhat-release ]; then
   cp maillog.service /usr/lib/systemd/system/
fi

if [ -f /etc/debian_version  ]; then
  cp maillog.service /lib/systemd/system/
fi
systemctl daemon-reload
systemctl enable maillog.service

echo "maillog is installed successfully"
echo "Configure /etc/maillog/maillog.conf"
echo "then run:  systemctl start maillog.service"



