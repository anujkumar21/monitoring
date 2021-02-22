import pytest
from kafka.errors import KafkaTimeoutError

from commons.constants import TOPIC, URL, REGEX, TEST_DATA
from services.kafka_producer.producer import Producer


class TestProducer:
    """
    This is to Producer.
    """

    def test_send_message(self):
        """
        Verify producer should send message properly.
        """
        producer = Producer()
        record_metadata = producer.send_message(TOPIC, URL, REGEX, TEST_DATA).get(timeout=5)
        assert record_metadata.topic == TOPIC, "Stats should be sent properly to topic {}.".format(TOPIC)

    def test_send_message_to_non_existing_topic(self):
        """
        Verify exception should occur is producer tries to send message to non existing topic.
        """
        producer = Producer()
        with pytest.raises(KafkaTimeoutError):
            producer.send_message("topic_not_exist", URL, REGEX, TEST_DATA)

    @pytest.mark.parametrize('url, status_code, regex, data, matched', (
            (URL, 200, REGEX, TEST_DATA, True),  # valid
            (URL, 200, REGEX, "INVALID TITLE", False),  # regex not matched
            (URL + "/searches?safe=abc", 404, REGEX, "Error 404 (Not Found)!!1", True),  # error code
            # proper metric should be created for valid, error response & in regex not matched cases.
    ))
    def test_create_request_metrics(self, url, status_code, regex, data, matched):
        """
        Verify metrics should be created properly.
        :param url: url
        :param status_code: status code
        :param regex: regular expression
        :param data: test data that need to be validated
        :param matched: True or False if data matched with regex
        """
        producer = Producer()
        stats = producer.create_request_metrics(url, regex, data)
        assert stats.status_code == status_code, \
            "Actual status code {} should be same as expected {}.".format(stats.status_code, status_code)
        assert stats.regex_pattern_matched == matched, \
            "Actual pattern matched {} should be same as expected {}.".format(stats.regex_pattern_matched, matched)
