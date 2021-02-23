# monitoring

## Description:

This utility monitors website availability over the network, produces metrics about this and passes these events through
an Aiven Kafka instance into an Aiven PostgreSQL database. It is implemented in python, and it runs on 2 different
docker containers.

Following metrics parameters are being fetched and stored in PostgreSQL database in monitoring table:

1. url: Website under monitoring
2. timestamp: Date time present in response header
3. status code: Response code
4. reason: Response message
5. response time: Response time
6. regex pattern matched: site data validation by regex

## Pre-Requisites:

1. Python 3.9
2. kafka-python 2.0.2
3. requests 2.25.1
4. psycopg2-binary 2.8.6
5. pytest 6.2.2
6. pytest-html-reporter 0.2.3
7. apscheduler 3.7.0
8. PyCharm or any other desired IDE

Kindly make sure

1. Aiven Kafka & PostgreSQL services should be running
2. Topic should be created as **'monitor'**

## How to invoke monitoring utility:

1. Clone project
   > git clone https://github.com/anujkumar21/monitoring.git
2. Navigate to root folder 'monitoring'
3. Install all required dependencies mentioned in requirements.txt using command
   > pip install -r requirements.txt
4. Copy your ca.pem, service.cert, service.key into [certs](https://github.com/anujkumar21/monitoring/tree/master/certs)
   folder
5. Update [config.ini](https://github.com/anujkumar21/monitoring/blob/master/resources/config.ini) file present in
   resources folder with server details
6. Run this utility(check topic 'monitor' should be present)

    1. Either via docker-compose.yml file.
       > docker-compose up
    2. Or via command, to run both producer & consumer services.
       > python services/kafka_producer/producer_runner.py

       > python services/kafka_consumer/consumer_runner.py

7. To execute test scripts
   > pytest -s -v -l

   Pytest html report is generated in root folder as pytest_html_report.html

   ![pytest_html_report](https://github.com/anujkumar21/monitoring/blob/master/test_report_screenshot.png)

## Enhancement:

1. Add more parameters in the metrics.
2. Implement proper way to shutdown producer/consumer running scheduler job.
3. Implement CI.
4. Better test coverage.
5. Improve Error Handling.

## References:

1. [Getting started with Aiven Kafka](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka)
2. [Getting started with Aiven PostgreSQL](https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql)
3. [kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html)
