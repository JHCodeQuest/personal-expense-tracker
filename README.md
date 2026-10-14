# CLI Expense Tracker

A command-line expense tracker built in Python. It uses `Decimal` for amounts, saves expenses to CSV, and validates user input.

## Requirements

- Python 3.8 or higher.
- No third-party packages are required.

## File Location and Storage

Expenses are stored in `expenses.csv` beside `main.py`. The application locates this file using `Path(__file__).resolve().parent`, regardless of the terminal's current directory.

The CSV column order is `date,description,category,amount`.

## How to Run

1. Ensure Python is installed.
2. Navigate to the folder containing `main.py`.
3. Run:

```bash
python main.py
```

## Usage Instructions

Choose an option from the menu:

1. **Add expense:** Enter a date in `DD/MM/YYYY` format, a non-empty description and category, and a finite amount greater than zero. The application saves after each addition.
2. **View all expenses:** Display a numbered list with amounts shown to two decimal places.
3. **Filter by category:** Find expenses using a case-insensitive category match.
4. **Show total:** Calculate the total using `Decimal` and display it to two decimal places.
5. **Save and quit:** Save expenses before exiting.

Invalid dates, blank descriptions or categories, and invalid amounts prompt you to try again.

## Known Limitations

- **Local, single-user storage:** Concurrent access and remote synchronisation are not supported.
- **Malformed CSV rows:** On startup, rows with missing columns or invalid amounts are reported and skipped. If any are found, the original CSV is copied to `expenses.bak` beside the script. Saving then writes only the loaded records and any new expenses.
- **Backup replacement:** A later startup that finds malformed rows can overwrite `expenses.bak`. Copy any backup you need to keep to another location before running the application again.
- **CSV validation:** The loader assumes the first row is a header. It does not validate header names, stored dates, or blank descriptions and categories. Extra columns are ignored.
- **Amount precision:** Amounts are not restricted to two decimal places, although displayed amounts are rounded to two places.
- **File errors:** File access and write failures are not handled with a recovery prompt.
- **Interface:** The application uses the terminal and has no graphical interface.
