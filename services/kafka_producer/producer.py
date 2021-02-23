import json
import re
from dataclasses import asdict
from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaProducer

from commons.config import Config
from commons.constants import SSL, CA_PEM, SERVICE_KEY, SERVICE_CERT, GMT_FORMAT, POLLING_TIME, TIMEOUT, TOPIC
from commons.log import log
from model.stats import Stats


class Producer:
    """
    This class is Kafka Producer class. It used initializing producer instance & has all related action methods.
    """

    def __init__(self):
        config = Config()
        service_uri = "{}:{}".format(config.get("host"), config.get("port"))
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=service_uri,
                security_protocol=SSL,
                ssl_cafile=CA_PEM,
                ssl_certfile=SERVICE_CERT,
                ssl_keyfile=SERVICE_KEY,
            )
        except Exception as ex:
            log.error("Please check kafka server is running & details are correctly mentioned in config.ini")
            log.error(ex)
            raise ex

    def send_message(self, topic, url, regex, data):
        """
        This method is used for sending message to kafka.
        :param topic: topic
        :param url: url
        :param regex: regular expression
        :param data: data need to be verified
        :return: future which can be used for meta-data
        """
        global future
        stats = self.create_request_metrics(url, regex, data)
        try:
            future = self.producer.send(topic, json.dumps(asdict(stats)).encode())
        except Exception as ex:
            log.error("Please check Kafka is running & has topic as '{}'".format(TOPIC))
            raise ex
        log.info("Message sent {}".format(future.get(timeout=TIMEOUT)))
        self.producer.flush()
        return future

    def send_messages_periodically(self, topic, url, regex, data):
        """
        This method is used for sending message to kafka periodically and used as cron job.
        :param topic: topic
        :param url: url
        :param regex: regular expression
        :param data: data need to be verified
        """
        scheduler = BlockingScheduler()
        scheduler.add_job(self.send_message, 'interval', seconds=POLLING_TIME, args=[topic, url, regex, data])
        scheduler.start()

    def create_request_metrics(self, url, regex, data):
        """
        This method is used for creating metrics for given url request.
        :param url: url
        :param regex: regular expression
        :param data: data that need to be verified with regex
        :return: Returns Stats object as metrics
        """
        response = requests.get(url, timeout=TIMEOUT)
        log.info("Requested url " + url)
        response_timestamp = datetime.strptime(response.headers.get('Date'), GMT_FORMAT).timestamp()
        stats = Stats()
        stats.url = url
        stats.timestamp = response_timestamp
        stats.status_code = response.status_code
        stats.reason = response.reason
        stats.response_time = response.elapsed.total_seconds()
        pattern = re.compile(regex)
        stats.regex_pattern_matched = data in re.findall(pattern, response.text)
        log.info("Metrics created: {}".format(stats))
        return stats
