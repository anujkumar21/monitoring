from commons.constants import TOPIC, URL, REGEX, TEST_DATA
from services.kafka_consumer.consumer import Consumer
from services.kafka_producer.producer import Producer
from services.postgresql.db_services import DBServices


class TestEndToEnd:
    """
    This is End to End(or Integration) test to test all 3 components - Kafka Producer, Kafka Consumer & PostgreSQL
    """

    def test_end_to_end(self):
        """
        Verify metrics is properly send & consumed in kafka via Producer & Consumer and stored to PostgreSQL.
        """
        producer = Producer()
        consumer = Consumer(TOPIC)
        db = DBServices()
        producer.send_message(TOPIC, URL, REGEX, TEST_DATA)
        # Consuming all messages & verifying one message to save test execution time
        stats = consumer.consume_and_store_messages()[0]
        row = dict(db.get_record_by("timestamp", stats.timestamp))
        assert stats.__dict__ == row, \
            "Kafka Consumed stats {} should be equal to PostgreSql stats {}".format(stats, row)
