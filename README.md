# Maillog_events


*Maillog_events* is designed to reveal email addresses by patterns and send to SQS (Amazon Simple Queue Service). 
If your mail server sometimes bulks emailing, you will be faced with the issues like "550 Message was not accepted -- invalid mailbox",  "451  user over quota" etc. It is not proper to send mail with an invalid mailbox, for example. You can get to a blacklist about that. You should delete or disable the email addresses with errors in your database. 


*maillog* is warking as a part of serverless architecture daemon to parse mail logs and send a message to exist SQS queue.   
The program has two configuration file */etc/maillog/maillog.conf* and */etc/maillog/pattern.xml* 
*maillog.conf* is main configuration file
*pattern.xml* is an xml file with patterns for pares log 

> Note: For full architecture, you have to write a SQS consumer and email addresses handler it will be different for different project, especially handler.


---

Please, install git and pip if you have not yet

##### For Debian like system 
```
apt update
apt install python-pip
apt install git

```

##### For Red Hat family tree
```
yum install python-pip
yum install git

```

##### Get the repository and install the program  

```
git clone https://github.com/ruslansvs2/maillog_events.git

cd maillog_events
pip install boto3 
pip install aws


./install.sh


``` 
> Note: Sometimes, occur problems with install modules through pip. In most cases, it is enough to upgrade an operating system.  
> 


Please, configure *emaillog* deamon in */etc/maillog/maillog.conf* file before start it. 

```
vim /etc/maillog/maillog.conf

```

```
[main]
# Path to mail log file
mail_log_file: /var/log/exim4/mainlog

# sleep time
sleep_time: 1

# Pattern file
pattern_file: /etc/maillog/pattern.xml

# AWS
# endpion - only for delete messange
endpoint_url: https://eu-west-1.queue.amazonaws.com/0000001
#
queue_name: email_errors

# credentials for AWS
aws_access_key_id: test
aws_secret_access_key: test
region_name: eu-west-1

# log O or 1
#logs sets loging messanges
# 0 - is disabled log messages
# 1 - is anabled log messages  
Logs: 1

```
Afer you sets proper data to the configuration file, you can add or delete patterns an XML file. 

```buildoutcfg
vim /etc/maillog/pattren.xml 

```
Just add or delete *event* block 

```buildoutcfg
<?xml version="1.0"?>
<data>
    <event>
        <number>1</number>
        <name>over quota</name>
        <pattern>The email account that you tried to reach is over quota</pattern>
    </event>
    <event>
        <number>2</number>
        <name>invalid mailbox</name>
        <pattern>invalid mailbox</pattern>
    </event>
</data>

```