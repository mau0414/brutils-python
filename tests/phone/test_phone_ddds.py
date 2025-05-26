from unittest import TestCase, main

from brutils.phone import (
    identify_ddd
)


class TestPhoneDDDs(TestCase):
    def test_invalid_ddds_and_numbers(self):
        self.assertEqual(identify_ddd("00"),{"error": "DDD 0 inválido."})
        self.assertEqual(identify_ddd("29999999999"), {"error": "DDD 29 inválido."})
        self.assertEqual(identify_ddd("119"),{"error": "Número de telefone inválido."})
        self.assertEqual(identify_ddd("11abc99999"), {"error": "Número de telefone inválido."})

    def test_valid_ddds_with_region(self):
        self.assertEqual(identify_ddd("11"), {
            "state": "São Paulo",
            "region": "Região Metropolitana de São Paulo"
        })
        self.assertEqual(identify_ddd("21"), {
            "state": "Rio de Janeiro",
            "region": "Região Metropolitana do Rio de Janeiro"
        })
        self.assertEqual(identify_ddd("85"),{
            "state": "Ceará",
            "region": "Região Metropolitana de Fortaleza"
        })
        self.assertEqual(identify_ddd("16"), {
            "state": "São Paulo",
            "region": "Região de Ribeirão Preto"
        })
        self.assertEqual(identify_ddd("38"), {
            "state": "Minas Gerais",
            "region": "Norte de Minas"
        })
        self.assertEqual(identify_ddd("46"),{
            "state": "Paraná",
            "region": "Sudoeste do Paraná"
        })

    def test_single_ddd_states(self):
        self.assertEqual(identify_ddd("82"), {
            "state": "Alagoas"
        })
        self.assertEqual(identify_ddd("63"), {
            "state": "Tocantins"
        })


    def test_valid_formats(self):
        self.assertEqual(identify_ddd("82"), {
            "state": "Alagoas"
        })
        self.assertEqual(identify_ddd("+5588996443006"), {
            "state": "Ceará",
            "region": "Sul do Ceará"
        })
        self.assertEqual(identify_ddd("5588996443006"), {
            "state": "Ceará",
            "region": "Sul do Ceará"
        })
        self.assertEqual(identify_ddd("(88) 99644-3006"), {
            "state": "Ceará",
            "region": "Sul do Ceará"
        })
        self.assertEqual(identify_ddd("88 99644 3006"), {
            "state": "Ceará",
            "region": "Sul do Ceará"
        })
        self.assertEqual(identify_ddd("65999999999"), {
            "state": "Mato Grosso",
            "region": "Região Metropolitana de Cuiabá"
        })

if __name__ == "__main__":
    main()
