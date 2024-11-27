#!/usr/bin/env python3
"""
A module that provides a function for obfuscating specific
fields in a log message.
"""

import re
from typing import List


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
