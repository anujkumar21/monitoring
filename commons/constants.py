from pathlib import Path

"""
This file contains all required constants.
"""

ROOT = str(Path(__file__).parent.parent)
SSL = "SSL"
CA_PEM = ROOT + "/certs/ca.pem"
SERVICE_CERT = ROOT + "/certs/service.cert"
SERVICE_KEY = ROOT + "/certs/service.key"
TOPIC = "monitor"
URL = "http://google.com"
REGEX = "<title[^>]*>([^<]+)</title>"
TEST_DATA = "Google"

POLLING_TIME = 30
TIMEOUT = 5

DB_SERVICE_URI = "postgres://{pg_user}:{pg_password}@{pg_host}:{pg_port}/defaultdb?sslmode=require"

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

TABLE_NAME = "monitoring"

CREATE_QUERY = """CREATE TABLE IF NOT EXISTS {} (
                       timestamp DOUBLE PRECISION,
                       url VARCHAR (40),
                       status_code INTEGER,
                       reason VARCHAR (40),
                       response_time DOUBLE PRECISION,
                       regex_pattern_matched BOOLEAN
                       );"""

TABLE_EXIST_QUERY = "select * from information_schema.tables where table_name=%s"

INSERT_QUERY = "insert into monitoring values (%s, %s, %s, %s, %s, %s);"

SELECT_QUERY = "select * from monitoring"

SELECT_WHERE_QUERY = "select * from monitoring where {} = {}"

DROP_QUERY = "drop table {}"
