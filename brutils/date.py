import re
from typing import Union
from num2words import num2words
from datetime import datetime
from brutils.data.enums.months import MonthsEnum

def convert_date_to_text(date: str) -> Union[str, None]:
    """
    Converts a given date in various formats to its textual representation.

    This function takes a date as a string in one of the supported formats and converts it
    to a string with the date written out in Brazilian Portuguese, including the full
    month name and the year.

    Args:
        date (str): The date to be converted into text. Supported formats:
                    dd/mm/yyyy, dd.mm.yyyy, dd-mm-yyyy, yyyy-mm-dd.

    Returns:
        str or None: A string with the date written out in Brazilian Portuguese,
        or None if the date is nonexistent.

    Raises:
        ValueError: If the input date string does not match any of the supported formats
    """

    supported_formats = {
        r"^\d{2}/\d{2}/\d{4}$": '%d/%m/%Y',  
        r"^\d{2}\.\d{2}\.\d{4}$": '%d.%m.%Y', 
        r"^\d{2}-\d{2}-\d{4}$": '%d-%m-%Y', 
        r"^\d{4}-\d{2}-\d{2}$": '%Y-%m-%d',    
    }

    matched_strptime_format = None

    for regex_pattern, strptime_format in supported_formats.items():
        if re.match(regex_pattern, date):
            matched_strptime_format = strptime_format
            break
    
    if not matched_strptime_format:
        raise ValueError(
            f"Date '{date}' has an invalid format. Please use one of the supported formats: dd/mm/yyyy, dd.mm.yyyy, dd-mm-yyyy, or YYYY-MM-DD."
        )

    dateObject = None
    try: 
        dateObject = datetime.strptime(date, matched_strptime_format)
    except ValueError:
        return None
    
    day = dateObject.day
    month = dateObject.month
    year = dateObject.year

    day_string = "Primeiro" if day == 1 else num2words(day, lang="pt")
    month_string = MonthsEnum(month).month_name
    year_string = num2words(year, lang="pt")

    date_string = (
        f"{day_string.capitalize()} de {month_string} de {year_string}"
    )

    return date_string