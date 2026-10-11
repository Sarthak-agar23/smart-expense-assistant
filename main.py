
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "expenses.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_expenses.csv"

REQUIRED_COLUMNS = ["date", "description", "category", "amount"]


def clean_expenses():
    if not INPUT_FILE.exists():
        print("Error: expenses.csv was not found.")
        return

    seen = set()
    cleaned_rows = []
    total_by_category = defaultdict(Decimal)
    total_expenses = Decimal("0")

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not all(
            column in reader.fieldnames
            for column in REQUIRED_COLUMNS
        ):
            print("Error: CSV headers are missing or incorrect.")
            return

        for line_number, row in enumerate(reader, start=2):
            try:
                date = (row.get("date") or "").strip()
                description = (
                    row.get("description") or ""
                ).strip()
                category = (row.get("category") or "").strip()
                amount_text = (row.get("amount") or "").strip()

                if not all([date, description, category, amount_text]):
                    print(f"Skipped row {line_number}: missing data.")
                    continue

                amount = Decimal(amount_text)

                if not amount.is_finite() or amount < 0:
                    print(f"Skipped row {line_number}: invalid amount.")
                    continue

                key = (
                    date, description.casefold(),
                    category.casefold(), amount
                )

                if key in seen:
                    print(f"Skipped row {line_number}: duplicate.")
                    continue

                seen.add(key)
                cleaned_rows.append({
                    "date": date,
                    "description": description,
                    "category": category,
                    "amount": str(amount),
                })

                total_expenses += amount
                total_by_category[category] += amount

            except InvalidOperation:
                print(f"Skipped row {line_number}: invalid amount.")
            except (ValueError, TypeError):
                print(f"Skipped row {line_number}: invalid data.")

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=REQUIRED_COLUMNS
        )
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("\n--- EXPENSE SUMMARY ---")
    print(f"Valid records: {len(cleaned_rows)}")
    print(f"Total expenses: Rs. {total_expenses:.2f}")
    print("\nExpenses by category:")

    for category, total in sorted(total_by_category.items()):
        print(f"{category}: Rs. {total:.2f}")

    print(f"\nCleaned data saved to: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    clean_expenses()
