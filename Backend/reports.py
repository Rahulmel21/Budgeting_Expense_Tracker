import csv
from datetime import datetime
from database import get_transactions


def validate_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return False, "Dates must use YYYY-MM-DD format."

    if start > end:
        return False, "Start date cannot be after end date."

    return True, "Date range is valid."

def get_transactions_by_date(user_id, start_date, end_date):
    valid, message = validate_date_range(start_date, end_date)
    if not valid:
        return [], message

    transactions = get_transactions(user_id)
    report_transactions = []

    for transaction in transactions:
        transaction_date = str(transaction.get("date", ""))
        if start_date <= transaction_date <= end_date:
            report_transactions.append(transaction)

    return report_transactions, "Transactions retrieved successfully."

def calculate_report_summary(user_id, start_date, end_date):
    transactions, message = get_transactions_by_date(
        user_id, start_date, end_date
    )

    if message != "Transactions retrieved successfully.":
        return None, message

    total_income = 0
    total_expenses = 0
    category_summary = {}

    for transaction in transactions:
        try:
            amount = float(transaction.get("amount", 0))
        except (ValueError, TypeError):
            amount = 0.0
        transaction_type = transaction.get("transactionType", "")
        category = transaction.get("category", "General")

        if transaction_type == "income":
            total_income += amount
        elif transaction_type == "expense":
            total_expenses += amount
            if category not in category_summary:
                category_summary[category] = 0
            category_summary[category] += amount

    balance = total_income - total_expenses

    summary = {
        "start_date": start_date,
        "end_date": end_date,
        "number_of_transactions": len(transactions),
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(balance, 2),
        "category_summary": {
            cat: round(amt, 2)
            for cat, amt in category_summary.items()
        }
    }
    return summary, "Report generated successfully."

def export_transactions_to_csv(
    user_id, start_date, end_date, filename="transaction_report.csv"
):
    transactions, message = get_transactions_by_date(
        user_id, start_date, end_date
    )

    if message != "Transactions retrieved successfully.":
        return False, message

    fieldnames = [
        "transactionID",
        "amount",
        "transactionType",
        "category",
        "date",
        "paymentMethod",
        "notes"
    ]
    
    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
                extrasaction="ignore"
            )
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(dict(transaction))

        return True, f"CSV report exported successfully: {filename}"

    except OSError:
        return False, "Could not create the CSV report."

def export_summary_to_csv(
    user_id, start_date, end_date, filename="summary_report.csv"
):
    summary, message = calculate_report_summary(
        user_id, start_date, end_date
    )

    if summary is None:
        return False, message

    try:
        with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Budget Tracker Report"])
            writer.writerow(["Start Date", summary["start_date"]])
            writer.writerow(["End Date", summary["end_date"]])
            writer.writerow([
            "Number of Transactions",
            summary["number_of_transactions"]
        ])

        writer.writerow(["Total Income", summary["total_income"]])
        writer.writerow(["Total Expenses", summary["total_expenses"]])
        writer.writerow(["Balance", summary["balance"]])
        writer.writerow([])
        writer.writerow(["Category", "Total Expenses"])

        for category, amount in summary["category_summary"].items():
            writer.writerow([category, amount])

        return True, f"Summary report exported successfully: {filename}"

    except OSError:
        return False, "Could not create the summary report."