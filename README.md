## A serverless architecture to pare and handling with mail logs

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Tasting](#testing)


## Introduction

*Maillog_events* is designed to reveal email addresses by patterns and send to SQS (Amazon Simple Queue Service). 
If your mail server sometimes bulks emailing, you will be faced with issues like *"550 Message was not accepted -- invalid mailbox"*,  *"451  user over quota"* etc. It is not proper to send mail with an invalid mailbox, for example. You can get to a blacklist about that. You should deleted or disabled the email addresses with errors in your database. 



*maillog* is working as a part of serverless architecture daemon to parse mail logs and send a message to SQS queue.   
The program has two configuration file */etc/maillog/maillog.conf* and */etc/maillog/pattern.xml* 

 - *maillog.conf* is main configuration file.
 - *pattern.xml* is an XML file with parse patterns. 

> Note: For full architecture, you have to write a SQS consumer and an email addresses handler it will be different for different project, especially handler.


---

## Installation
 
Please, install git and pip if you have not yet.
> Note: You should be root or have high privileges. 

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
Please, you have to configure /etc/maillog/maillog.conf
then run:  systemctl start maillog.service
maillog is installed successfully


``` 
> Note: Sometimes, occur problems with install modules through pip. In most cases, it is enough to upgrade an operating system.  
> 

## Configuration 
Please, configure the *emaillog* daemon in the */etc/maillog/maillog.conf* file before start it. 

Use following command or other console editor for configure it. 
```
vim /etc/maillog/maillog.conf

```

```
[main]
# Path to mail log file
mail_log_file: /var/log/exim4/mainlog

# sleep time in second
sleep_time: 120

# Pattern file
pattern_file: /etc/maillog/pattern.xml

# AWS
# endpion - only for delete message
endpoint_url: https://eu-west-1.queue.amazonaws.com/0000001
#
queue_name: email_errors

# credentials for AWS
aws_access_key_id: test
aws_secret_access_key: test
region_name: eu-west-1

# log O or 1
#logs sets logging messanges
# 0 - is disabled log messages
# 1 - is enabled log messages  
Logs: 1

```
After you sets proper data to the configuration file, you can add or delete patterns an XML file. 

Open the file to write. 
```buildoutcfg
vim /etc/maillog/pattern.xml 

```
Just add or delete *event* block. 

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
At the end, start the daemon. 

```buildoutcfg
systemctl start maillog

```
## Tasting
 

For testing, you need turn on logs for daemon into the configuration file and restart it.

```buildoutcfg
sed  's/Logs: 0/Logs:\ 1/' /etc/maillog/maillog.conf 

systemctl restart maillog

```
Check the daemon's logs.

```buildoutcfg
systemctl status  maillog

journalctl -u maillog

```
If you don't see error messages you can write data with your pattern into a mail server's log file.  

Following command you write to mail's log *"over quota"* pattren.
```buildoutcfg

echo '2018-07-17 04:41:15 1fdHyN-00061Y-LL == test@gmail.com R=dnslookup T=remote_smtp defer (-44): SMTP error from remote mail server after RCPT TO:<test2.gmail.com>: host alt4.gmail-smtp-in.l.google.com [127.0.0.1]: 452-4.2.2 The email account that you tried to reach is over quota. Please direct\n452-4.2.2 the recipient to\n452 4.2.2  https://support.google.com/mail/?p=OverQuotaTemp s13-v6si24815369jam.8 - gsmtp' >> /var/log/exim4/mainlog

```

After a few time you can see into you syslog.

```buildoutcfg
journalctl -u maillog

Sep  9 01:01:40 mail1 maillog.add_to_queue: ID:a6519db1-2453-4152-dcb6-a83fd7a29aw1 {"email": "test2@gmail.com", "hostname": "mail1.test.com", "ID": "1", "name": "over quota"}

```

If you see this message evrything is working properly. Of course, for more sure, you can check the SQS queue. Below you can see an example.  
```
aws sqs receive-message --queue-url  https://regin.queue.amazonaws.com/00000001/email_errors   --attribute-names All --message-attribute-names All --max-number-of-messages 1

```