# maillog_events

maillog - is a deamon to parse mail logs and send messange to SQS (Amazon Simple Queue Service)  
The program has two configuration file /etc/maillog/maillog.conf and /etc/maillog/pattern.xml 
maillog.conf is main configuration file
pattern.xml is a xml file with pattern for pares log 


Please, install git and pip if you have not yet

For Debina like system 
```
apt update
apt install python-pip
apt install git

```

For Red Hat family tree
```
yum install python-pip
yun install git

```

Get the repository and install the program  

```
git clone https://github.com/ruslansvs2/maillog_events.git

cd maillog_events
pip install boto3 
pip install aws


./install.sh


``` 

Please, configure /etc/maillog/maillog.conf before start deamon. 




