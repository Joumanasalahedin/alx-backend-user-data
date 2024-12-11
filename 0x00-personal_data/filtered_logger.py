#!/usr/bin/env python3
"""
Module for filtering and obfuscating sensitive data in log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specific fields in a log message.
    Returns:
        The obfuscated log message.
    """
    pattern = f"({'|'.join(map(re.escape, fields))})=.*?{re.escape(separator)}"
    return re.sub(pattern, lambda m:
                  f"{m.group(1)}={redaction}{separator}", message)
