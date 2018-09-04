# maillog_events

maillog - is a daemon to parse mail logs and send a message to SQS (Amazon Simple Queue Service)  
The program has two configuration file /etc/maillog/maillog.conf and /etc/maillog/pattern.xml 
maillog.conf is main configuration file
pattern.xml is a xml file with patterns for pares log 


Please, install git and pip if you have not yet

For Debian like system 
```
apt update
apt install python-pip
apt install git

```

For Red Hat family tree
```
yum install python-pip
yum install git

```

Get the repository and install the program  

```
git clone https://github.com/ruslansvs2/maillog_events.git

cd maillog_events
pip install boto3 
pip install aws


./install.sh


``` 
> Note: Sometimes, occur problems with install modules through pip. In most cases, it is enough to upgrade an operating system.  
> 


Please, configure /etc/maillog/maillog.conf before start daemon. 




