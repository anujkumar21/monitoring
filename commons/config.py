from configparser import ConfigParser

from commons.constants import ROOT


class Config:
    """
    This class is to read config file.
    """

    def __init__(self):
        self.config = ConfigParser()
        self.config_file = ROOT + "/resources/config.ini"

    def get(self, key, section="kafka"):
        """
        This method is to get values from config file.
        :param key: key
        :param section: section e.g. kafka or postgresql
        :return: value
        """
        self.config.read(self.config_file)
        return self.config.get(section, key)
