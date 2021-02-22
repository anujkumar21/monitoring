import json
from dataclasses import dataclass


@dataclass
class Stats:
    """
    This class is used as response metrics format.
    """
    url: str
    timestamp: float
    status_code: int
    reason: str
    response_time: float
    regex_pattern_matched: bool = False

    def __init__(self, json_value=None):
        if json_value is not None:
            self.__dict__ = json.loads(json_value)
