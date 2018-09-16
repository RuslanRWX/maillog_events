## A serverless architecture to pare and handling with mail logs

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Tasting](#testing)


## Introduction

*Maillog_events* is a producer that designed to reveal email addresses by patterns and send to [SQS](https://aws.amazon.com/sqs/) (Amazon Simple Queue Service). If your mail server sends email in bulk, you will fase issues like *"550 Message was not accepted -- invalid mailbox","451 user over quota"* etc. It is not proper to send mail with an invalid mailbox, for example. You can get blacklisted for that. You should delete or disable the email addresses with errors in your database.


![alt text](https://raw.githubusercontent.com/ruslansvs2/maillog_events/master/mail_events_produser.jpg)

*maillog* works as a part of serverless architecture daemon to parse mail logs and sends messages to [SQS](https://aws.amazon.com/sqs/) queue.

The program has two configuration files: /etc/maillog/maillog.conf and /etc/maillog/pattern.xml
 - *maillog.conf* is main configuration file.
 - *pattern.xml* is an [XML](https://en.wikipedia.org/wiki/XML) file with parse patterns. 

> Note: For full event-driven architecture, you have to write a SQS consumer and an email addresses handler. They are not included into the tool.

---

## Installation
 
Please, install [GIT](https://git-scm.com/) and [PIP](https://pypi.org/project/pip/) if you have not yet.
> Note: You should be root or have high privileges. 

##### For [Debian-based](https://www.debian.org/) distributions: 
```
apt update
apt install python-pip
apt install git

```

##### For [Red Hat](https://www.redhat.com) family tree:
```
yum install python-pip
yum install git

```

##### Get the repository and install the program:

```
git clone https://github.com/ruslansvs2/maillog_events.git

cd maillog_events
pip install boto3 
pip install aws


./install.sh
maillog is installed successfully
Configure /etc/maillog/maillog.conf
then run:  systemctl start maillog.service


``` 
> Note: Sometimes, occur problems with install modules through pip. In most cases, it is enough to upgrade an operating system.  
> 

## Configuration 

Configure the *maillog* daemon in the */etc/maillog/maillog.conf* file before starting it.

Use the following command or other console editor to configure it. 
```
vim /etc/maillog/maillog.conf

```

```
[main]
# Path to mail log file
mail_log_file: /var/log/exim4/mainlog

# sleep time in seconds
sleep_time: 120

# Pattern file
pattern_file: /etc/maillog/pattern.xml

# AWS
# endpoint - only for deleting message
endpoint_url: https://eu-west-1.queue.amazonaws.com/0000001
#
queue_name: email_errors

# credentials for AWS
aws_access_key_id: test
aws_secret_access_key: test
region_name: eu-west-1

# log O or 1
#logs sets logging messages
# 0 - is disabled log messages
# 1 - is enabled log messages  
Logs: 1
```
After you sets proper data to the configuration file, you can add or delete patterns in an XML file. 

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
In the end, start the daemon. 

```buildoutcfg
systemctl start maillog

```
## Testing
 

For testing, you need to turn on logs for daemon into the configuration file and restart it.

```buildoutcfg
sed -i 's/Logs:\ 0/Logs:\ 1/' /etc/maillog/maillog.conf 

systemctl restart maillog

```
Check the daemon logs.

```buildoutcfg
systemctl status  maillog

journalctl -u maillog

```
If you don't see error messages, you can write data with your pattern into a mail server's log file.

Use this command:
```buildoutcfg

echo '2018-07-17 04:41:15 1fdHyN-00061Y-LL == test@gmail.com R=dnslookup T=remote_smtp defer (-44): SMTP error from remote mail server after RCPT TO:<test2.gmail.com>: host alt4.gmail-smtp-in.l.google.com [127.0.0.1]: 452-4.2.2 The email account that you tried to reach is over quota. Please direct\n452-4.2.2 the recipient to\n452 4.2.2  https://support.google.com/mail/?p=OverQuotaTemp s13-v6si24815369jam.8 - gsmtp' >> /var/log/exim4/mainlog

```

If everything works properly, after some time you will see the following in *syslog*:

```buildoutcfg
journalctl -u maillog

Sep  9 01:01:40 mail1 maillog.add_to_queue: ID:a6519db1-2453-4152-dcb6-a83fd7a29aw1 {"email": "test2@gmail.com", "hostname": "mail1.test.com", "ID": "1", "name": "over quota"}

```

If you see this message, everything is working properly. To be 100%  sure, you can check the SQS queue. Below you can see an example:

```
aws sqs receive-message --queue-url  https://regin.queue.amazonaws.com/00000001/email_errors   --attribute-names All --message-attribute-names All --max-number-of-messages 1

```
