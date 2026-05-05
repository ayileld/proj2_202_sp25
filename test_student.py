import unittest
from proj2 import *


class TestProject2(unittest.TestCase):

    def test_parse_float_empty(self):
        self.assertEqual(parse_float(""), None)

    def test_parse_float_number(self):
        self.assertEqual(parse_float("12.5"), 12.5)

    def test_read_csv_lines_length(self):
        data = read_csv_lines("sample.csv")
        self.assertEqual(listlen(data), 6)

    def test_first_row_country(self):
        data = read_csv_lines("sample.csv")
        self.assertEqual(data.value.country, "Andorra")

    def test_missing_data_is_none(self):
        data = read_csv_lines("sample.csv")
        self.assertEqual(data.value.energy_co2_emissions, None)

    def test_filter_country_equal(self):
        data = read_csv_lines("sample.csv")
        result = filter_rows(data, "country", "equal", "Canada")
        self.assertEqual(listlen(result), 2)

    def test_filter_greater_than(self):
        data = read_csv_lines("sample.csv")
        result = filter_rows(data, "energy_co2_emissions", "greater_than", 500)
        self.assertEqual(listlen(result), 3)

    def test_filter_less_than(self):
        data = read_csv_lines("sample.csv")
        result = filter_rows(data, "total_co2_emissions_excluding_lucf", "less_than", 400)
        self.assertEqual(listlen(result), 2)

    def test_filter_skips_none(self):
        data = read_csv_lines("sample.csv")
        result = filter_rows(data, "energy_co2_emissions", "less_than", 100)
        self.assertEqual(listlen(result), 0)

    def test_country_less_than_error(self):
        data = read_csv_lines("sample.csv")
        with self.assertRaises(ValueError):
            filter_rows(data, "country", "less_than", "Canada")


if __name__ == "__main__":
    unittest.main()

