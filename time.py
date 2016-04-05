#!/usr/bin/env python
"""Utilities for dealing with timestamps

Functions:
    fix_sixtysec: Fix timestamps where we have seconds==60
"""
from datetime import datetime, timedelta


def fix_sixtysec(timestamp):
    """Fix timestamp if seconds==60.

    Use datetime and timedelta to fix a timestamp that is mistakenly
    timestamped as HH:MM:60 (as it should wrap around to HH:MM+1:00)

    Args:
        timestamp (string): Timestamp to fix
    """
    fixed = timestamp
    if ':60' in timestamp:
        timestamp = timestamp.replace(":60", ":59")
        dt = datetime.strptime(timestamp, "%d/%m/%y %H:%M:%S.%f")
        fixed = dt + timedelta(seconds=1)
    return fixed.strftime("%d/%m/%y %H:%M:%S.%f")


def fix_all_sixtysec(timestamps):
    """Fix a list of timestamps that include HH:MM:60.

    Run fix_sixtysec over the entire list, fixing if needed.

    Args:
        timestamps ([string]): list of timestamps

    Returns:
        ([string]): list of fixed timestamps
    """
    return list(map(fix_sixtysec, timestamps))
