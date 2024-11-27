#!/usr/bin/env python3
"""
A logging module that redacts sensitive personal information (PII)
from log messages.
"""

import logging
import re
from typing import Tuple

# Define PII fields from the given CSV structure
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger to redact sensitive information.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """
    Formatter class that redacts PII fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str, ...]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields (Tuple[str, ...]): Tuple of fields to redact in the logs.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and redacted log message.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)


def filter_datum(fields: Tuple[str, ...],
                 redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.

    Args:
        fields (Tuple[str, ...]): Tuple of field names to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message to process.
        separator (str): The field separator.

    Returns:
        str: The obfuscated log message.
    """
    pattern = r"({})=([^{}]*)".format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
