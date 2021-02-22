from datetime import datetime

from commons.constants import URL
from model.stats import Stats
from services.postgresql.db_services import DBServices


class TestPostgreSQL:
    """
    This is to test DBServices for PostgreSQL.
    """

    def test_create_table(self, table_name="monitoring"):
        """
        Verify given table should be create properly.
        :param table_name: table name
        """
        db = DBServices()
        db.create_table()

        # Verifying table was created successfully
        assert db.is_table_present(table_name), table_name + " should be created."

    def test_insert_record(self):
        """
        Verify metrics should be stored successfully.
        """
        stats = Stats()
        stats.timestamp = float(datetime.now().strftime("%s"))
        stats.url = URL
        stats.status_code = 200
        stats.reason = "OK"
        stats.response_time = 0.072123
        stats.regex_pattern_matched = True

        db = DBServices()
        db.insert_into(stats)
        row = dict(db.get_record_by("timestamp", stats.timestamp))
        assert row == stats.__dict__, "Actual stats {} should be same as expected {}.".format(row, stats)

    def test_drop_table(self, table_name="monitoring"):
        """
        Verify given table should be dropped successfully.
        :param table_name: table name
        """
        db = DBServices()
        db.drop_table(table_name)

        # Verifying table was deleted successfully
        assert not db.is_table_present(table_name), table_name + " should be deleted."
