#!/usr/bin/env python3
"""
Filtered logger module
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces specified fields in the log message with redaction.
    """
    pattern = re.compile(r'({})=[^{}]*'.format('|'.join(fields), re.escape(separator)))
    return pattern.sub(r'\1={}'.format(redaction), message)
