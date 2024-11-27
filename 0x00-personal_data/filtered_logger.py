#!/usr/bin/env python3
"""
A module that provides a function for obfuscating specific
fields in a log message.
"""

import logging
import re
from typing import List, Tuple


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): The string to be replaced in the field values with.
        message (str): Log message
        separator (str): The field separato

    Returns:
        str: Obfuscated log message.
    """
    pattern = r'({})=([^{}]*)'.format('|'.join(map(
        re.escape, fields)), re.escape(separator))
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for sensitive information filtering. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields (Tuple[str]): Tuple of fields to redact in the logs.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        # Convert tuple to list for compatibility with filter_datum
        self.fields = list(fields)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating sensitive fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and redacted log message.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)
