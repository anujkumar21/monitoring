import os
import sys

sys.path.append(os.path.dirname(os.curdir))

from commons.constants import TOPIC
from services.kafka_consumer.consumer import Consumer

"""
This is to run consumer cron job.
"""

consumer = Consumer(TOPIC)
consumer.get_messages_periodically()
