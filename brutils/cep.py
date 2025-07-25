from json import loads
from random import randint
from unicodedata import normalize
from urllib.request import urlopen

from brutils.data.enums import UF
from brutils.exceptions import CEPNotFound, InvalidCEP
from brutils.types import Address

# FORMATTING
############

def _is_valid_format(cep): # type: (str) -> bool
    """
    (Internal helper) Checks if a CEP string has a valid format (8 digits).
    """
    return isinstance(cep, str) and len(cep) == 8 and cep.isdigit()


def remove_symbols(dirty):  # type: (str) -> str
    """
    Removes specific symbols from a given CEP (Postal Code).

    This function takes a CEP (Postal Code) as input and removes all occurrences
    of the '.' and '-' characters from it.

    Args:
        cep (str): The input CEP (Postal Code) containing symbols to be removed.

    Returns:
        str: A new string with the specified symbols removed.

    Example:
        >>> remove_symbols("123-45.678.9")
        "123456789"
        >>> remove_symbols("abc.xyz")
        "abcxyz"
    """

    return "".join(filter(lambda char: char not in ".-", dirty))


def format_cep(cep):  # type: (str) -> str | None
    """
    Formats a Brazilian CEP (Postal Code) into a standard format.

    This function takes a CEP (Postal Code) as input and, if it is a valid
    8-digit CEP, formats it into the standard "12345-678" format.

    Args:
        cep (str): The input CEP (Postal Code) to be formatted.

    Returns:
        str: The formatted CEP in the "12345-678" format if it's valid,
             None if it's not valid.

    Example:
        >>> format_cep("12345678")
        "12345-678"
        >>> format_cep("12345")
        None
    """

    return f"{cep[:5]}-{cep[5:8]}" if _is_valid_format(cep) else None


# OPERATIONS
############


def is_valid(cep, check_existence: bool = False): # type: (str, bool) -> bool
    """
    Checks if a Brazilian CEP (Postal Code) is valid.

    By default, this function only validates the CEP's format, checking if the
    input is a string containing exactly 8 digits.

    When the `check_existence` parameter is set to True, the function performs
    an additional check to confirm if the CEP corresponds to a real-world address.

    Args:
        cep (str): The string containing the CEP to be checked.
        check_existence (bool): If True, also validates the real-world
                                existence of the CEP. Defaults to False.

    Returns:
        bool: True if the CEP is valid, False otherwise.
    """

    if not _is_valid_format(cep):
        return False

    if not check_existence:
        return True

    return get_address_from_cep(cep) is not None

def generate():  # type: () -> str
    """
    Generates a random 8-digit CEP (Postal Code) number as a string.

    Returns:
        str: A randomly generated 8-digit number.

    Example:
        >>> generate()
        "12345678"
    """

    generated_number = ""

    for _ in range(8):
        generated_number = generated_number + str(randint(0, 9))

    return generated_number


# Reference: https://viacep.com.br/
def get_address_from_cep(cep, raise_exceptions=False):  # type: (str, bool) -> Address | None
    """
    Fetches address information from a given CEP (Postal Code) using the ViaCEP API.

    Args:
        cep (str): The CEP (Postal Code) to be used in the search.
        raise_exceptions (bool, optional): Whether to raise exceptions when the CEP is invalid or not found. Defaults to False.

    Raises:
        InvalidCEP: When the input CEP is invalid.
        CEPNotFound: When the input CEP is not found.

    Returns:
        Address | None: An Address object (TypedDict) containing the address information if the CEP is found, None otherwise.

    Example:
        >>> get_address_from_cep("12345678")
        {
            "cep": "12345-678",
            "logradouro": "Rua Example",
            "complemento": "",
            "bairro": "Example",
            "localidade": "Example",
            "uf": "EX",
            "ibge": "1234567",
            "gia": "1234",
            "ddd": "12",
            "siafi": "1234"
        }

        >>> get_address_from_cep("abcdefg")
        None

        >>> get_address_from_cep("abcdefg", True)
        InvalidCEP: CEP 'abcdefg' is invalid.

        >>> get_address_from_cep("00000000", True)
        CEPNotFound: 00000000
    """
    base_api_url = "https://viacep.com.br/ws/{}/json/"

    clean_cep = remove_symbols(cep)
    cep_is_valid = _is_valid_format(clean_cep) 

    if not cep_is_valid:
        if raise_exceptions:
            raise InvalidCEP(cep)

        return None

    try:
        with urlopen(base_api_url.format(clean_cep)) as f:
            response = f.read()
            data = loads(response)

            if data.get("erro", False):
                raise CEPNotFound(cep)

            return Address(**loads(response))

    except Exception as e:
        if raise_exceptions:
            raise CEPNotFound(cep) from e

        return None


def get_cep_information_from_address(
    federal_unit, city, street, raise_exceptions=False
):  # type: (str, str, str, bool) -> list[Address] | None
    """
    Fetches CEP (Postal Code) options from a given address using the ViaCEP API.

    Args:
        federal_unit (str): The two-letter abbreviation of the Brazilian state.
        city (str): The name of the city.
        street (str): The name (or substring) of the street.
        raise_exceptions (bool, optional): Whether to raise exceptions when the address is invalid or not found. Defaults to False.

    Raises:
        ValueError: When the input UF is invalid.
        CEPNotFound: When the input address is not found.

    Returns:
        list[Address] | None: A list of Address objects (TypedDict) containing the address information if the address is found, None otherwise.

    Example:
        >>> get_cep_information_from_address("EX", "Example", "Rua Example")
        [
            {
                "cep": "12345-678",
                "logradouro": "Rua Example",
                "complemento": "",
                "bairro": "Example",
                "localidade": "Example",
                "uf": "EX",
                "ibge": "1234567",
                "gia": "1234",
                "ddd": "12",
                "siafi": "1234"
            }
        ]

        >>> get_cep_information_from_address("A", "Example", "Rua Example")
        None

        >>> get_cep_information_from_address("XX", "Example", "Example", True)
        ValueError: Invalid UF: XX

        >>> get_cep_information_from_address("SP", "Example", "Example", True)
        CEPNotFound: SP - Example - Example
    """
    if federal_unit in UF.values:
        federal_unit = UF(federal_unit).name

    if federal_unit not in UF.names:
        if raise_exceptions:
            raise ValueError(f"Invalid UF: {federal_unit}")

        return None

    base_api_url = "https://viacep.com.br/ws/{}/{}/{}/json/"

    parsed_city = (
        normalize("NFD", city)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .replace(" ", "%20")
    )
    parsed_street = (
        normalize("NFD", street)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .replace(" ", "%20")
    )

    try:
        with urlopen(
            base_api_url.format(federal_unit, parsed_city, parsed_street)
        ) as f:
            response = f.read()
            response = loads(response)

            if len(response) == 0:
                raise CEPNotFound(f"{federal_unit} - {city} - {street}")

            return [Address(**address) for address in response]

    except Exception as e:
        if raise_exceptions:
            raise CEPNotFound(f"{federal_unit} - {city} - {street}") from e

        return None