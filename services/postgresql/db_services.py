import psycopg2
from psycopg2.extras import RealDictCursor

from commons.config import Config
from commons.constants import INSERT_QUERY, CREATE_QUERY, TABLE_NAME, SELECT_WHERE_QUERY, DROP_QUERY, \
    TABLE_EXIST_QUERY, DB_SERVICE_URI
from commons.log import log


class DBServices:
    """
    This class is used connecting PostgreSQL & has all related action methods.
    """

    def __init__(self):
        config = Config()
        self.uri = DB_SERVICE_URI.format(pg_user=config.get('pg_user', 'postgresql'),
                                         pg_password=config.get('pg_password', 'postgresql'),
                                         pg_host=config.get('pg_host', 'postgresql'),
                                         pg_port=config.get('pg_port', 'postgresql'))
        self.connection = psycopg2.connect(self.uri)

    def create_table(self):
        """
        This method is used for creating table.
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(CREATE_QUERY.format(TABLE_NAME))
        except Exception as ex:
            log.error("Table not created.")
            log.error(ex)
        finally:
            cursor.close()
            self.connection.commit()

    def insert_into(self, stats):
        """
        This method is used for inserting metrics into table.
        :param stats: metrics as Stats object
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(INSERT_QUERY, (stats.timestamp, stats.url, stats.status_code, stats.reason,
                                          stats.response_time, stats.regex_pattern_matched))
            log.info("Message stored in db: {}".format(stats))
        except Exception as ex:
            log.error("Stats not inserted.")
            log.error(ex)
        finally:
            cursor.close()
            self.connection.commit()

    def get_record_by(self, column, value):
        """
        This method is used for fetching all matched records from PostgreSQL.
        :param column: column name
        :param value: value
        :return: list of all matched records
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(SELECT_WHERE_QUERY.format(column, value))
            records = cursor.fetchone()
            log.info("Record fetched: {}".format(records))
            return records
        except Exception as ex:
            log.error("Record not fetched.")
            log.error(ex)
        finally:
            cursor.close()
            self.connection.commit()

    def drop_table(self, table_name):
        """
        This method is used for dropping table
        :param table_name: table name
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(DROP_QUERY.format(table_name))
        except Exception as ex:
            log.error("Table not dropped.")
            log.error(ex)
        finally:
            cursor.close()
            self.connection.commit()

    def is_table_present(self, table_name):
        """
        This method is to check table present or not.
        :param table_name: table name
        :return: bool
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(TABLE_EXIST_QUERY, (table_name,))
            return bool(cursor.rowcount)
        except Exception as ex:
            log.error("Find table query not executed.")
            log.error(ex)
        finally:
            cursor.close()
            self.connection.commit()
