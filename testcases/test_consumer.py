import pytest

from commons.constants import URL, REGEX, TEST_DATA, TOPIC
from services.kafka_consumer.consumer import Consumer
from services.kafka_producer.producer import Producer


class TestConsumer:
    """
    This is to test Consumer
    """

    @pytest.mark.parametrize('url, status_code, regex, data', (
            (URL, 200, REGEX, TEST_DATA),
            (URL + "/searches?safe=abc", 404, REGEX, "Error 404 (Not Found)!!1"),
    ))
    def test_consume_and_store_messages(self, url, status_code, regex, data):
        """
        Verify message is properly consumed from kafka
        :param url: url
        :param status_code: status code
        :param regex: regular expression
        :param data: test data
        """
        producer = Producer()
        consumer = Consumer(TOPIC)
        producer.send_message(TOPIC, url, regex, data)
        stats_lst = consumer.consume_and_store_messages()
        for stats in stats_lst:
            if stats.url == url:
                assert stats.status_code == status_code, \
                    "Actual status code {} should be same as expected {}".format(stats.status_code, status_code)

    def test_consume_messages_from_non_existing_topic(self, topic="does_not_exist"):
        """
        Verify message count should be Zero, if topic does not exist.
        :param topic: invalid topic
        """
        consumer = Consumer(topic)
        assert len(consumer.consume_and_store_messages()) == 0, "Message count should be 0, for non existing topic"
