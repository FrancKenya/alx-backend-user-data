#!/usr/bin/env python3
"""
A module used to obfuscate sensitive information in logs.
"""

import logging
from typing import List
from re import sub


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    The filter_datum function obfuscates specific fields in a log message.

    Args:
        fields (List[str]): List of fields to redact in the log message.
        redaction (str): The string to replace the field's value with.
        message (str): The log message to obfuscate.
        separator (str): The separator between fields in the log message.

    Returns:
        str: The log message.
    """
    pattern = r'({})=([^{}]*)'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ A class used to obfuscate sensitive information in logs. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to redact in the logs.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
       Usef to format the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and redacted log message.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)
