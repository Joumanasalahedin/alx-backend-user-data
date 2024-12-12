#!/usr/bin/env python3
"""
Module for filtering and obfuscating sensitive data in log messages.
"""

import logging
from typing import List
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields: List of fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive fields.
        Returns:
            The formatted and redacted log record.
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger instance for user data with sensitive fields redacted.

    Returns:
        A logging.Logger object configured with a RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connects to a MySQL database using credentials from environment variables.

    Returns:
        A MySQLConnection object for interacting with the database.
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn


def main() -> None:
    """
    Main function to log user data with sensitive fields filtered.

    Retrieves rows from the users table and logs sensitive fields redacted.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM users;")
        columns = [column[0] for column in cursor.description]
        for row in cursor:
            record = "; ".join(
                f"{key}={value}" for key, value in zip(columns, row)
            )
            logger.info(record)
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
