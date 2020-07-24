# Immobilienscout-crawler
Given a query link this project automatically crawls the data and sends automatic email notification if new apartments are present.

## Usage

We can use crontab to schedule a crawling job on regular intervals.

* export ADDR=\<query-address>
* export SENDER=\<email-address>
* crontab -e
* Add the line -- */\<interval> * * * * cd <repository-dir> && /usr/local/bin/python3.7 main.py --addr $ADDR --sender $SENDER
* Check the scheduled jobs using crontab -l

## Dependencies

Please check https://developers.google.com/gmail/api/quickstart/python to get the necessary permissions.