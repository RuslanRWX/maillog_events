# maillog 

maillog - is a deamon to parse mail logs and send messange to SQS (Amazon Simple Queue Service)  
The program has two configuration file /etc/maillog/maillog.conf and /etc/maillog/pattern.xml 
maillog.conf is main configuration file
pattern.xml is a xml file with pattern for pares log 

get the repository and install the program  

```
git https://github.com/ruslansvs2/maillog_events.git

cd maillog_events

./install.sh

pip install boto3 
pip install aws
``` 






