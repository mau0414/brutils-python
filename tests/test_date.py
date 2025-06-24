from unittest import TestCase

from num2words import num2words

from brutils import convert_date_to_text
from brutils.data.enums.months import MonthsEnum


class TestNum2Words(TestCase):
    def test_num_conversion(self) -> None:
        """
        Smoke test of the num2words library.
        This test is used to guarantee that our dependency still works.
        """
        self.assertEqual(num2words(30, lang="pt-br"), "trinta")
        self.assertEqual(num2words(42, lang="pt-br"), "quarenta e dois")
        self.assertEqual(
            num2words(2024, lang="pt-br"), "dois mil e vinte e quatro"
        )
        self.assertEqual(num2words(0, lang="pt-br"), "zero")
        self.assertEqual(num2words(-1, lang="pt-br"), "menos um")


class TestDate(TestCase):
    # Valid and right format dates 
    def test_valid_dates_conversion(self):
        self.assertEqual(convert_date_to_text("15/08/2024"),"Quinze de agosto de dois mil e vinte e quatro")
        self.assertEqual(convert_date_to_text("01/01/2000"),"Primeiro de janeiro de dois mil") # First day of the year
        self.assertEqual(convert_date_to_text("31/12/1999"),"Trinta e um de dezembro de mil novecentos e noventa e nove") # Last day of the year
        self.assertEqual(convert_date_to_text("29/02/2020"),"Vinte e nove de fevereiro de dois mil e vinte") # Leap year
        self.assertEqual(convert_date_to_text("01/03/2025"),"Primeiro de marco de dois mil e vinte e cinco") # First day of the month

    # Nonexistent dates
    def test_nonexistent_dates(self):
        self.assertIsNone(convert_date_to_text("31/04/2025"))  #April has 30 days
        self.assertIsNone(convert_date_to_text("29/02/2025"))  # Non-leap year
        self.assertIsNone(convert_date_to_text("29/02/2025"))  # Non-leap year

    # Invalid day numbers
    def test_invalid_day_numbers(self):
        self.assertIsNone(convert_date_to_text("00/01/2025"))
        self.assertIsNone(convert_date_to_text("32/01/2025"))
   
    # Invalid month numbers
    def test_invalid_month_numbers(self):
        self.assertIsNone(convert_date_to_text("15/00/2025"))
        self.assertIsNone(convert_date_to_text("15/13/2025"))

    # Invalid alternative formats
    def test_invalid_formats(self):
        self.assertRaises(ValueError, convert_date_to_text, "Invalid")
        self.assertRaises(ValueError, convert_date_to_text, "15-08-2025")  
        self.assertRaises(ValueError, convert_date_to_text, "15.08.2025")  
        self.assertRaises(ValueError, convert_date_to_text, "2025-01-22")  
        self.assertRaises(ValueError, convert_date_to_text, "25/1/2020")  
        self.assertRaises(ValueError, convert_date_to_text, "19/08/20") 
        self.assertRaises(ValueError, convert_date_to_text, "5/09/2020")  
        self.assertRaises(ValueError, convert_date_to_text, "1924/08/20")


    months_year = [
        (1, "janeiro"),
        (2, "fevereiro"),
        (3, "marco"),
        (4, "abril"),
        (5, "maio"),
        (6, "junho"),
        (7, "julho"),
        (8, "agosto"),
        (9, "setembro"),
        (10, "outubro"),
        (11, "novembro"),
        (12, "dezembro"),
    ]

    def testMonthEnum(self):
        for number_month, name_month in self.months_year:
            month = MonthsEnum(number_month)
            self.assertEqual(month.month_name, name_month)
