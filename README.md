# maillog_events


maillog_events is designed to reveal email addresses by patterns and send to SQS (Amazon Simple Queue Service). 
If your mail server sometimes bulks emailing, you will be faced with the issues like "550 Message was not accepted -- invalid mailbox",  "451  user over quota" etc. It is not proper to send mail with an invalid mailbox, for example. You can get to a blacklist about that. You should delete or disable the email addresses with errors in your database. 


maillog is warking as a part of serverless architecture daemon to parse mail logs and send a message to exist SQS queue.   
The program has two configuration file /etc/maillog/maillog.conf and /etc/maillog/pattern.xml 
maillog.conf is main configuration file
pattern.xml is a xml file with patterns for pares log 

> Note: For full architecture, you have to write a SQS consumer and email addresses handler it will be different for different project, especially handler.


---

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




