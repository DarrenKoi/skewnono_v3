from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from typing import Optional, Union
import re

def parse_date_string(
    date_string: str, 
    return_iso: bool = False,
    include_microseconds: bool = True
) -> Optional[Union[datetime, str]]:
    """
    Convert various date string formats to datetime object or ISO format string.
    
    Args:
        date_string: Input date string in various formats
        return_iso: If True, returns ISO format string; if False, returns datetime object
        include_microseconds: If False, removes microseconds from the result
        
    Returns:
        datetime object or ISO format string, or None if parsing fails
    """
    
    if not date_string or not isinstance(date_string, str):
        return None
    
    # Clean up the input string
    date_string = date_string.strip()
    
    # Handle relative dates first
    relative_dt = parse_relative_date(date_string)
    if relative_dt:
        if not include_microseconds:
            relative_dt = relative_dt.replace(microsecond=0)
        return relative_dt.isoformat() if return_iso else relative_dt
    
    # Try dateutil parser
    try:
        # Common date hints for ambiguous formats
        # Set dayfirst=True for European format (DD/MM/YYYY)
        # You can change this based on your primary user base
        dt = parser.parse(date_string, fuzzy=True, dayfirst=False)
        if not include_microseconds:
            dt = dt.replace(microsecond=0)
        return dt.isoformat() if return_iso else dt
    except (parser.ParserError, ValueError):
        pass
    
    # Try with dayfirst=True for European formats
    try:
        dt = parser.parse(date_string, fuzzy=True, dayfirst=True)
        if not include_microseconds:
            dt = dt.replace(microsecond=0)
        return dt.isoformat() if return_iso else dt
    except (parser.ParserError, ValueError):
        pass
    
    return None


def parse_relative_date(date_string: str) -> Optional[datetime]:
    """Parse relative date strings like 'today', 'yesterday', '3 days ago', etc."""
    date_string_lower = date_string.lower()
    now = datetime.now()
    
    # Simple relative dates
    relative_dates = {
        'today': now,
        'now': now,
        'yesterday': now - relativedelta(days=1),
        'tomorrow': now + relativedelta(days=1),
        'last week': now - relativedelta(weeks=1),
        'next week': now + relativedelta(weeks=1),
        'last month': now - relativedelta(months=1),
        'next month': now + relativedelta(months=1),
        'last year': now - relativedelta(years=1),
        'next year': now + relativedelta(years=1),
    }
    
    if date_string_lower in relative_dates:
        return relative_dates[date_string_lower]
    
    # Parse "X days/weeks/months/years ago" or "in X days/weeks/months/years"
    patterns = [
        (r'(\d+)\s*days?\s*ago', lambda x: now - relativedelta(days=int(x))),
        (r'(\d+)\s*weeks?\s*ago', lambda x: now - relativedelta(weeks=int(x))),
        (r'(\d+)\s*months?\s*ago', lambda x: now - relativedelta(months=int(x))),
        (r'(\d+)\s*years?\s*ago', lambda x: now - relativedelta(years=int(x))),
        (r'in\s*(\d+)\s*days?', lambda x: now + relativedelta(days=int(x))),
        (r'in\s*(\d+)\s*weeks?', lambda x: now + relativedelta(weeks=int(x))),
        (r'in\s*(\d+)\s*months?', lambda x: now + relativedelta(months=int(x))),
        (r'in\s*(\d+)\s*years?', lambda x: now + relativedelta(years=int(x))),
    ]
    
    for pattern, func in patterns:
        match = re.search(pattern, date_string_lower)
        if match:
            return func(match.group(1))
    
    return None


def parse_date_string_with_settings(
    date_string: str, 
    return_iso: bool = False,
    dayfirst: bool = False,
    yearfirst: bool = False,
    default: Optional[datetime] = None,
    include_microseconds: bool = True
) -> Optional[Union[datetime, str]]:
    """
    Advanced version with more control over parsing behavior.
    
    Args:
        date_string: Input date string
        return_iso: If True, returns ISO format string
        dayfirst: If True, interprets 01/05/2024 as May 1st (European format)
        yearfirst: If True, interprets the first value as year
        default: Default datetime for missing components
        include_microseconds: If False, removes microseconds from the result
        
    Returns:
        datetime object or ISO format string, or None if parsing fails
    """
    
    if not date_string or not isinstance(date_string, str):
        return None
    
    date_string = date_string.strip()
    
    # Handle relative dates
    relative_dt = parse_relative_date(date_string)
    if relative_dt:
        if not include_microseconds:
            relative_dt = relative_dt.replace(microsecond=0)
        return relative_dt.isoformat() if return_iso else relative_dt
    
    try:
        dt = parser.parse(
            date_string, 
            fuzzy=True, 
            dayfirst=dayfirst,
            yearfirst=yearfirst,
            default=default
        )
        if not include_microseconds:
            dt = dt.replace(microsecond=0)
        return dt.isoformat() if return_iso else dt
    except (parser.ParserError, ValueError):
        return None


# Example usage and test cases
if __name__ == "__main__":
    # Note: You need to install python-dateutil first:
    # pip install python-dateutil
    
    test_dates = [
        "2024-01-15",
        "15/01/2024",
        "01/15/2024",
        "January 15, 2024",
        "15 Jan 2024",
        "2024-01-15T14:30:00Z",
        "2024-01-15 14:30:00",
        "15-Jan-2024",
        "20240115",
        "today",
        "yesterday",
        "tomorrow",
        "3 days ago",
        "in 5 days",
        "last week",
        "next month",
        "2 years ago",
        "15:30",
        "3:30 PM",
        "on 15th January 2024",
        "the 15th of January, 2024",
        "Jan 15",  # Will use current year
        "Monday",  # Will find next Monday
        "March 2023",
        "Q1 2024",  # Won't parse
    ]
    
    print("Testing various date formats with dateutil:\n")
    for date_str in test_dates:
        result = parse_date_string(date_str)
        iso_result = parse_date_string(date_str, return_iso=True)
        print(f"Input: '{date_str}'")
        print(f"DateTime: {result}")
        print(f"ISO Format: {iso_result}")
        print("-" * 50)
    
    # Test with different settings
    print("\n\nTesting with different settings:")
    ambiguous_date = "05/01/2024"
    
    us_format = parse_date_string_with_settings(ambiguous_date, dayfirst=False)
    eu_format = parse_date_string_with_settings(ambiguous_date, dayfirst=True)
    
    print(f"\nAmbiguous date: '{ambiguous_date}'")
    print(f"US format (MM/DD/YYYY): {us_format}")
    print(f"EU format (DD/MM/YYYY): {eu_format}")
    
    # Test microseconds handling
    print("\n\nTesting microseconds handling:")
    precise_time = "2024-01-15T14:30:45.123456"
    
    with_micro = parse_date_string(precise_time, return_iso=True, include_microseconds=True)
    without_micro = parse_date_string(precise_time, return_iso=True, include_microseconds=False)
    
    print(f"\nInput with microseconds: '{precise_time}'")
    print(f"With microseconds: {with_micro}")
    print(f"Without microseconds: {without_micro}")
    
    # Test with 'now' to show microsecond removal
    now_with = parse_date_string("now", return_iso=True, include_microseconds=True)
    now_without = parse_date_string("now", return_iso=True, include_microseconds=False)
    
    print(f"\n'now' with microseconds: {now_with}")
    print(f"'now' without microseconds: {now_without}")