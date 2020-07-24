# Immobilienscout-crawler
Given a query link this project automatically crawls the data and sends automatic email notification if new apartments are present.

## Usage

We can use crontab to schedule a crawling job on regular intervals.

* ```bash export ADDR=<query-address> ```
* ```bash export SENDER=<email-address> ```
* ```bash crontab -e ```
* Add the line ```bash */<interval> * * * * cd <repository-dir> && /usr/local/bin/ python3.7 main.py --addr $ADDR --sender $SENDER ```
* Check the scheduled jobs using ```bash crontab -l ```

## Dependencies

Please check https://developers.google.com/gmail/api/quickstart/python to get the necessary permissions.