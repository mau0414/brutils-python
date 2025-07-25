import re
from random import choice, randint

from brutils.data.ddd_to_regions import DDD_TO_REGION
from brutils.data.ddd_to_uf import DDD_TO_UF, UFS_WITH_SINGLE_DDD


# FORMATTING
############
def format_phone(phone):  # type: (str) -> str
    """
    Function responsible for formatting a telephone number

    Args:
        phone_number (str): The phone number to format.

    Returns:
        str: The formatted phone number, or None if the number is not valid.


    >>> format_phone("11994029275")
    '(11)99402-9275'
    >>> format_phone("1635014415")
    '(16)3501-4415'
    >>> format_phone("333333")
    """
    if not is_valid(phone):
        return None

    ddd = phone[:2]
    phone_number = phone[2:]

    return f"({ddd}){phone_number[:-4]}-{phone_number[-4:]}"


# OPERATIONS
############


def is_valid(phone_number, type=None):  # type: (str, str) -> bool
    """
    Returns if a Brazilian phone number is valid.
    It does not verify if the number actually exists.

    Args:
        phone_number (str): The phone number to validate.
                            Only digits, without country code.
                            It should include two digits DDD.
        type (str): "mobile" or "landline".
                    If not specified, checks for one or another.

    Returns:
        bool: True if the phone number is valid. False otherwise.
    """

    if type == "landline":
        return _is_valid_landline(phone_number)
    if type == "mobile":
        return _is_valid_mobile(phone_number)

    return _is_valid_landline(phone_number) or _is_valid_mobile(phone_number)


def remove_symbols_phone(phone_number):  # type: (str) -> str
    """
    Removes common symbols from a Brazilian phone number string.

    Args:
        phone_number (str): The phone number to remove symbols.
                            Can include two digits DDD.

    Returns:
        str: A new string with the specified symbols removed.
    """

    cleaned_phone = (
        phone_number.replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace("+", "")
        .replace(" ", "")
    )
    return cleaned_phone


def generate(type=None):  # type: (str) -> str
    """
    Generate a valid and random phone number.

    Args:
        type (str): "landline" or "mobile".
                    If not specified, checks for one or another.

    Returns:
        str: A randomly generated valid phone number.

    Example:
        >>> generate()
        "2234451215"
        >>> generate("mobile")
        "1899115895"
        >>> generate("landline")
        "5535317900"
    """

    if type == "mobile":
        return _generate_mobile_phone()

    if type == "landline":
        return _generate_landline_phone()

    generate_functions = [_generate_landline_phone, _generate_mobile_phone]
    return choice(generate_functions)()


def remove_international_dialing_code(phone_number):  # type: (str) -> str
    """
    Function responsible for remove a international code phone

    Args:
        phone_number (str): The phone number with international code phone.

    Returns:
        str: The phone number without international code
            or the same phone number.

    Example:
    >>> remove_international_dialing_code("5511994029275")
    '11994029275'
    >>> remove_international_dialing_code("1635014415")
    '1635014415'
    >>> remove_international_dialing_code("+5511994029275")
    '+11994029275'
    """

    pattern = r"\+?55"

    if (
        re.search(pattern, phone_number)
        and len(phone_number.replace(" ", "")) > 11
    ):
        return phone_number.replace("55", "", 1)
    else:
        return phone_number


def identify_ddd(phone_number: str):
    """
    Identifies the area code of a Brazilian telephone number and returns the state
    and, if applicable, the corresponding metropolitan region.

    Args:
    phone_number (str): The telephone number to identify the area code from.
                        It can include the country code, may contain symbols (such as +, -, or spaces),
                        or be just the two-digit area code (DDD).

    Returns:
    dict: Containing 'state' and optionally 'region', or error.

    Example:
        >>> identify_ddd('11')
        {'state': 'São Paulo', 'region': 'Região Metropolitana de São Paulo'}
        >>> identify_ddd('65999999999')
        {'state': 'Mato Grosso', 'region': 'Norte de Mato Grosso'}
        >>> identify_ddd('82')
        {'state': 'Alagoas'}
        >>> identify_ddd('00')
        {'error': 'DDD 0 inválido.'}
        >>> identify_ddd('29999999999')
        {'error': 'DDD 29 inválido.'}
        >>> identify_ddd('5588997889955')
        {'state': 'Ceará', 'region': 'Sul do Ceará'}
        >>> identify_ddd('+5588996443006')
        {'state': 'Ceará', 'region': 'Sul do Ceará'}
    """

    phone_number = remove_symbols_phone(phone_number)

    if phone_number.isdigit() and len(phone_number) == 2:
        ddd = int(phone_number)
    else:
        phone_number_clean = remove_international_dialing_code(phone_number)
        if not is_valid(phone_number_clean):
            return {"error": "Número de telefone inválido."}

        ddd = int(_extract_ddd_from_phone(phone_number_clean))

    uf = DDD_TO_UF.get(ddd)

    if uf is None:
        return {
            "error": f"DDD {ddd} inválido."
        }

    if uf in UFS_WITH_SINGLE_DDD:
        return {
            "state": uf.value
        }

    region = DDD_TO_REGION.get(ddd)

    return {
        "state": uf.value,
        "region": region
    }


def _extract_ddd_from_phone(phone_number: str):  # type: (str) -> (str)
    """
    Extracts the DDD (area code) from a Brazilian phone number.

    Removes the international dialing code (if present) and returns the
    first two digits of the local number, which correspond to the DDD.

    Args:
        phone_number (str): The phone number, with or without an international dialing code.
                            It must contain at least two digits after the code is removed.

    Returns:
        str: The two-digit DDD (area code).
    """

    cleaned_phone_number = remove_international_dialing_code(phone_number)
    return cleaned_phone_number[:2]


def _is_valid_mobile(phone_number: str):  # type: (str) -> bool
    """
    Returns if a Brazilian mobile number is valid.
    It does not verify if the number actually exists.

    Args:
        phone_number (str): The mobile number to validate.
                            Only digits, without country code.
                            It should include two digits DDD.

    Returns:
        bool: True if the phone number is valid. False otherwise.
    """

    pattern = re.compile(r"^[1-9][1-9][9]\d{8}$")
    return (
        isinstance(phone_number, str)
        and re.match(pattern, phone_number) is not None
    )


def _is_valid_landline(phone_number: str):  # type: (str) -> bool
    """
    Returns if a Brazilian landline number is valid.
    It does not verify if the number actually exists.

    Args:
        phone_number (str): The landline number to validate.
                            Only digits, without country code.
                            It should include two digits DDD.

    Returns:
        bool: True if the phone number is valid. False otherwise.
    """

    pattern = re.compile(r"^[1-9][1-9][2-5]\d{7}$")
    return (
        isinstance(phone_number, str)
        and re.match(pattern, phone_number) is not None
    )


def _generate_ddd_number():  # type() -> str
    """
    Generate a valid DDD number.
    """
    return f'{"".join([str(randint(1, 9)) for i in range(2)])}'


def _generate_mobile_phone():
    """
    Generate a valid and random mobile phone number
    """
    ddd = _generate_ddd_number()
    client_number = [str(randint(0, 9)) for i in range(8)]

    phone_number = f'{ddd}9{"".join(client_number)}'

    return phone_number


def _generate_landline_phone():  # type () -> str
    """
    Generate a valid and random landline phone number.
    """
    ddd = _generate_ddd_number()
    return f"{ddd}{randint(2,5)}{str(randint(0,9999999)).zfill(7)}"
