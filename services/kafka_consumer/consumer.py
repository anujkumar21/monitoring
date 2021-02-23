from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaConsumer

from commons.config import Config
from commons.constants import CA_PEM, SERVICE_CERT, SERVICE_KEY, SSL, POLLING_TIME
from commons.log import log
from model.stats import Stats
from services.postgresql.db_services import DBServices


class Consumer:
    """
    This class is Kafka Consumer class. It used initializing consumer instance & has all related action methods.
    """

    def __init__(self, topic):
        config = Config()
        try:
            service_uri = "{}:{}".format(config.get("host"), config.get("port"))
            self.consumer = KafkaConsumer(
                topic,
                auto_offset_reset="earliest",
                bootstrap_servers=service_uri,
                client_id="demo-client-1",
                group_id="demo-group",
                security_protocol=SSL,
                ssl_cafile=CA_PEM,
                ssl_certfile=SERVICE_CERT,
                ssl_keyfile=SERVICE_KEY,
            )
        except Exception as ex:
            log.error("Please check kafka server is running & details are correctly mentioned in config.ini")
            raise ex

    def consume_and_store_messages(self):
        """
        This method is for consuming all the messages from kafka & storing it to postgresql.
        :return: list of stats (response metrics)
        """
        stats_lst = []
        for _ in range(2):
            raw_msgs = self.consumer.poll(timeout_ms=1000)
            for tp, msgs in raw_msgs.items():
                for msg in msgs:
                    stats_lst.append(Stats(msg.value))
                    log.info("Message consumed: {}".format(msg.value))
        self.consumer.commit()
        db = DBServices()
        db.create_table()
        for stats in stats_lst:
            db.insert_into(stats)

        return stats_lst

    def get_messages_periodically(self):
        """
        This method is for consuming all the messages from kafka & storing it to postgresql periodically.
        It is used as cron job.
        """
        scheduler = BlockingScheduler()
        scheduler.add_job(self.consume_and_store_messages, 'interval', seconds=POLLING_TIME)
        scheduler.start()
