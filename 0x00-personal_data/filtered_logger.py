#!/usr/bin/env python3
"""
Filtered logger module
"""


import re

def filter_datum(fields: list[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces specified fields in the log message with redaction.
    """
    return re.sub(r'(?<={}=).*?(?={})'.format('|'.join(fields), re.escape(separator)), redaction, message)

