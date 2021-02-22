import os
import sys

sys.path.append(os.path.dirname(os.curdir))

from commons.constants import URL, TOPIC, REGEX, TEST_DATA
from services.kafka_producer.producer import Producer

"""
This is to run producer cron job.
"""
producer = Producer()
producer.send_messages_periodically(TOPIC, URL, REGEX, TEST_DATA)
