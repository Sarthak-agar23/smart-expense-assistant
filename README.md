# Smart Expense & CSV Assistant

A beginner-friendly Python project that reads expense records from a CSV file, validates the data, skips invalid or duplicate records, calculates spending totals, and writes cleaned records to a new CSV file.

## Features

- Reads expense records from `expenses.csv`
- Checks that the required CSV columns are present
- Skips rows with missing fields
- Skips rows with invalid or negative amounts
- Detects duplicate records
- Calculates total expenses and totals by category
- Exports valid records to `cleaned_expenses.csv`
- Uses Python's `Decimal` for expense amounts

## Technologies

- Python 3
- `csv` for reading and writing CSV files
- `decimal` for monetary arithmetic
- `collections.defaultdict` for category totals
- `pathlib` for file paths

## Project files

```text
smart-expense-assistant/
├── README.md
├── main.py
├── expenses.csv
└── cleaned_expenses.csv   # generated when the program runs
```

## Requirements

- Python 3
- No third-party Python packages are required

## How to run

1. Download or clone this repository.
2. Make sure `main.py` and `expenses.csv` are in the same folder.
3. Open PowerShell or a terminal in that folder.
4. Run:

   ```bash
   python main.py
   ```

   On Windows, `py main.py` can also be used if the `python` command is unavailable.

The program creates or replaces `cleaned_expenses.csv` in the project folder.

## Sample data and expected results

The included example data has six valid records, one repeated-looking bus-fare entry on a different date, one row with a missing description, and one row with an invalid amount (`abc`). Because the bus-fare entries have different dates, they are not duplicates according to the program's current duplicate rule.

Expected summary for the original sample data:

| Result | Expected value |
|---|---:|
| Valid records | 6 |
| Total expenses | Rs. 729.00 |
| Education | Rs. 230.00 |
| Food | Rs. 120.00 |
| Travel | Rs. 80.00 |
| Utilities | Rs. 299.00 |

The incomplete row and invalid-amount row are skipped. The program only skips a duplicate when the date, description, category, and amount all match an earlier row.

## Limitations

- The program expects the CSV file to contain the columns `date`, `description`, `category`, and `amount`.
- Duplicate detection considers all four fields; identical purchases on different dates are treated as separate records.
- This is a learning and portfolio project, not accounting software. Review results before using any data for real financial decisions.
- The included sample data is fictional. Do not commit private or client financial data to a public repository.

## Possible future improvements

- Add automated tests
- Support configurable input and output filenames
- Produce monthly summaries
- Generate charts of expenses by category
- Add a simple graphical user interface

## Automated Tests

The project includes unit tests written with Python's built-in `unittest` framework.

The tests check:

- Expense totals and record counts
- Duplicate detection
- Invalid amounts
- Missing required data
- Missing input files
- Incorrect CSV headers

### Run the Tests

```bash
python -m unittest -v test_main.py
```

All tests should pass before a release is considered ready.

## Author

Sarthak Agarwal
