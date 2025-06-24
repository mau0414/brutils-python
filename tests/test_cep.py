from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from brutils.cep import (
    CEPNotFound,
    InvalidCEP,
    format_cep,
    generate,
    get_address_from_cep,
    get_cep_information_from_address,
    is_valid,
    remove_symbols,
)


class TestCEP(TestCase):
    def test_remove_symbols(self):
        self.assertEqual(remove_symbols("00000000"), "00000000")
        self.assertEqual(remove_symbols("01310-200"), "01310200")
        self.assertEqual(remove_symbols("01..310.-200.-"), "01310200")
        self.assertEqual(remove_symbols("abc01310200*!*&#"), "abc01310200*!*&#")
        self.assertEqual(
            remove_symbols("ab.c1.--.3-102.-0-.0-.*.-!*&#"), "abc1310200*!*&#"
        )
        self.assertEqual(remove_symbols("...---..."), "")

    def test_is_valid(self):

        # Invalid types (when CEP is not string, returns False)
        self.assertFalse(is_valid(1))  # Number
        self.assertFalse(is_valid(None))  # None
        self.assertFalse(is_valid([]))  # Array
        
        # Invalid lengths (when CEP's len is different of 8, returns False)
        self.assertFalse(is_valid(""))  # Empty
        self.assertFalse(is_valid("1"))  # Lower boundary 
        self.assertFalse(is_valid("1234567"))  # Below boundary (7 digits)
        self.assertFalse(is_valid("123456789"))  # Above boundary (9 digits)
        self.assertFalse(is_valid("1234567890"))  # Above boundary (10 digits)
        
        # Invalid characters (when CEP does not contain only digits, returns False)
        self.assertFalse(is_valid("1234-678"))  # Hyphen
        self.assertFalse(is_valid("1234 5678"))  # Space
        self.assertFalse(is_valid("1234A678"))  # Letter
        self.assertFalse(is_valid("1234.6789"))  # Dot
        
        # Valid CEPs
        self.assertTrue(is_valid("00000000"))  
        self.assertTrue(is_valid("99999999"))  
        self.assertTrue(is_valid("12345678"))  
        self.assertTrue(is_valid("18052780"))  # Real CEP

    def test_generate(self):
        for _ in range(10_000):
            self.assertIs(is_valid(generate()), True)


@patch("brutils.cep.is_valid")
class TestIsValidToFormat(TestCase):
    def test_when_cep_is_valid_returns_True_to_format(self, mock_is_valid):
        mock_is_valid.return_value = True

        self.assertEqual(format_cep("01310200"), "01310-200")

        # Checks if function is_valid_cnpj is called
        mock_is_valid.assert_called_once_with("01310200")

    def test_when_cep_is_not_valid_returns_none(self, mock_is_valid):
        mock_is_valid.return_value = False

        # When cep isn't valid, returns None
        self.assertIsNone(format_cep("013102009"))


@patch("brutils.cep.urlopen")
class TestCEPAPICalls(TestCase):
    @patch("brutils.cep.loads")
    def test_get_address_from_cep_success(self, mock_loads, mock_urlopen):
        mock_loads.return_value = {"cep": "01310-200"}

        self.assertEqual(
            get_address_from_cep("01310200", True), {"cep": "01310-200"}
        )

    def test_get_address_from_cep_raise_exception_invalid_cep(
        self, mock_urlopen
    ):
        mock_data = MagicMock()
        mock_data.read.return_value = {"erro": True}
        mock_urlopen.return_value = mock_data

        self.assertIsNone(get_address_from_cep("013102009"))

    def test_get_address_from_cep_invalid_cep_raise_exception_invalid_cep(
        self, mock_urlopen
    ):
        with self.assertRaises(InvalidCEP):
            get_address_from_cep("abcdef", True)

    def test_get_address_from_cep_invalid_cep_raise_exception_cep_not_found(
        self, mock_urlopen
    ):
        mock_data = MagicMock()
        mock_data.read.return_value = {"erro": True}
        mock_urlopen.return_value = mock_data

        with self.assertRaises(CEPNotFound):
            get_address_from_cep("01310209", True)

    @patch("brutils.cep.loads")
    def test_get_cep_information_from_address_success(
        self, mock_loads, mock_urlopen
    ):
        mock_loads.return_value = [{"cep": "01310-200"}]

        self.assertDictEqual(
            get_cep_information_from_address(
                "SP", "Example", "Rua Example", True
            )[0],
            {"cep": "01310-200"},
        )

    @patch("brutils.cep.loads")
    def test_get_cep_information_from_address_success_with_uf_conversion(
        self, mock_loads, mock_urlopen
    ):
        mock_loads.return_value = [{"cep": "01310-200"}]

        self.assertDictEqual(
            get_cep_information_from_address(
                "São Paulo", "Example", "Rua Example", True
            )[0],
            {"cep": "01310-200"},
        )

    @patch("brutils.cep.loads")
    def test_get_cep_information_from_address_empty_response(
        self, mock_loads, mock_urlopen
    ):
        mock_loads.return_value = []

        self.assertIsNone(
            get_cep_information_from_address("SP", "Example", "Rua Example")
        )

    @patch("brutils.cep.loads")
    def test_get_cep_information_from_address_raise_exception_invalid_cep(
        self, mock_loads, mock_urlopen
    ):
        mock_loads.return_value = {"erro": True}

        self.assertIsNone(
            get_cep_information_from_address("SP", "Example", "Rua Example")
        )

    def test_get_cep_information_from_address_invalid_cep_dont_raise_exception_invalid_uf(
        self, mock_urlopen
    ):
        self.assertIsNone(
            get_cep_information_from_address("ABC", "Example", "Rua Example")
        )

    def test_get_cep_information_from_address_invalid_cep_raise_exception_invalid_uf(
        self, mock_urlopen
    ):
        with self.assertRaises(ValueError):
            get_cep_information_from_address(
                "ABC", "Example", "Rua Example", True
            )

    def test_get_cep_information_from_address_invalid_cep_raise_exception_cep_not_found(
        self, mock_urlopen
    ):
        mock_response = MagicMock()
        mock_response.read.return_value = {"erro": True}
        mock_urlopen.return_value = mock_response

        with self.assertRaises(CEPNotFound):
            get_cep_information_from_address(
                "SP", "Example", "Rua Example", True
            )


if __name__ == "__main__":
    main()
