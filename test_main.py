
import contextlib
import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class ExpenseAssistantTests(unittest.TestCase):

    def run_program(self, csv_content=None, missing_file=False):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            input_file = folder / "expenses.csv"
            output_file = folder / "cleaned_expenses.csv"

            if not missing_file:
                input_file.write_text(
                    csv_content,
                    encoding="utf-8"
                )

            output = io.StringIO()

            with patch.object(main, "INPUT_FILE", input_file), \
                 patch.object(main, "OUTPUT_FILE", output_file), \
                 contextlib.redirect_stdout(output):
                main.clean_expenses()

            result = output.getvalue()

            cleaned_rows = []
            if output_file.exists():
                with output_file.open(
                    newline="", encoding="utf-8"
                ) as file:
                    cleaned_rows = list(csv.DictReader(file))

            return result, cleaned_rows

    def test_correct_totals(self):
        data = (
            "date,description,category,amount\n"
            "2026-10-01,Book,Education,150\n"
            "2026-10-02,Bus,Travel,40\n"
            "2026-10-03,Lunch,Food,120\n"
        )

        output, rows = self.run_program(data)

        self.assertIn("Valid records: 3", output)
        self.assertIn("Total expenses: Rs. 310.00", output)
        self.assertEqual(len(rows), 3)

    def test_duplicate_is_skipped(self):
        data = (
            "date,description,category,amount\n"
            "2026-10-01,Book,Education,150\n"
            "2026-10-01,Book,Education,150\n"
        )

        output, rows = self.run_program(data)

        self.assertIn("duplicate", output)
        self.assertIn("Valid records: 1", output)
        self.assertIn("Total expenses: Rs. 150.00", output)
        self.assertEqual(len(rows), 1)

    def test_invalid_amount_is_skipped(self):
        data = (
            "date,description,category,amount\n"
            "2026-10-01,Book,Education,abc\n"
            "2026-10-02,Bus,Travel,40\n"
        )

        output, rows = self.run_program(data)

        self.assertIn("invalid amount", output)
        self.assertIn("Valid records: 1", output)
        self.assertIn("Total expenses: Rs. 40.00", output)
        self.assertEqual(len(rows), 1)

    def test_missing_description_is_skipped(self):
        data = (
            "date,description,category,amount\n"
            "2026-10-01,,Food,50\n"
            "2026-10-02,Bus,Travel,40\n"
        )

        output, rows = self.run_program(data)

        self.assertIn("missing data", output)
        self.assertIn("Valid records: 1", output)
        self.assertEqual(len(rows), 1)

    def test_missing_input_file(self):
        output, rows = self.run_program(missing_file=True)

        self.assertIn("expenses.csv was not found", output)
        self.assertEqual(rows, [])

    def test_incorrect_headers(self):
        data = (
            "date,description,category\n"
            "2026-10-01,Book,Education\n"
        )

        output, rows = self.run_program(data)

        self.assertIn("headers are missing or incorrect", output)
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
