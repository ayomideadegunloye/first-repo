"""Expense Tracker: a small command line app for tracking your spending.

Usage examples:
    python tracker.py add 12.50 food "Lunch at the campus cafe"
    python tracker.py list
    python tracker.py total
    python tracker.py delete 1

Data is saved in expenses.json next to this file.

Currency symbol: set the TRACKER_CURRENCY environment variable to change it.
    TRACKER_CURRENCY="£" python tracker.py list
"""

import argparse
import json
import os
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "expenses.json"
CURRENCY = os.environ.get("TRACKER_CURRENCY", "$")


def load_expenses():
    """Return the list of saved expenses (empty list if none yet)."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_expenses(expenses):
    """Write the list of expenses to disk."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount, category, note=""):
    """Add a new expense and return it."""
    expenses = load_expenses()
    expense = {
        "id": max((e["id"] for e in expenses), default=0) + 1,
        "amount": amount,
        "category": category.lower(),
        "note": note,
        "date": date.today().isoformat(),
    }
    expenses.append(expense)
    save_expenses(expenses)
    return expense


def list_expenses():
    """Return all expenses."""
    return load_expenses()


def total_spent():
    """Return the total amount spent across all expenses.

    TODO (Task 1): implement this function.
    """
    raise NotImplementedError("total_spent is not built yet")


def delete_expense(expense_id):
    """Delete the expense with the given id.

    Return True if something was deleted, False if the id was not found.

    TODO (Task 2): implement this function.
    """
    raise NotImplementedError("delete_expense is not built yet")


def build_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add an expense")
    add.add_argument("amount", type=float)
    add.add_argument("category")
    add.add_argument("note", nargs="?", default="")

    sub.add_parser("list", help="show all expenses")
    sub.add_parser("total", help="show total spent")

    delete = sub.add_parser("delete", help="delete an expense by id")
    delete.add_argument("id", type=int)

    sub.add_parser("calculate")

    return parser


def main():
    args = build_parser().parse_args()

    # this part implements what happens when you select one of the arguments
    try:
        if args.command == "add":
            e = add_expense(args.amount, args.category, args.note)
            print(f"Added #{e['id']}: {CURRENCY}{e['amount']:,.2f} on {e['category']}")

        elif args.command == "list":
            expenses = list_expenses()
            if not expenses:
                print("No expenses yet.")
            for e in expenses:
                amount = f"{CURRENCY}{e['amount']:,.2f}"
                print(
                    f"#{e['id']} {e['date']}  {amount:>12}  "
                    f"{e['category']:<12} {e['note']}"
                )

        elif args.command == "total":
            print(f"Total spent: {CURRENCY}{total_spent():,.2f}")

        elif args.command == "delete":
            if delete_expense(args.id):
                print(f"Deleted #{args.id}")
            else:
                print(f"No expense with id {args.id}")

        elif args.command == "calculate":
            print("This is the calculate argument")

    except NotImplementedError as err:
        print(f"Not built yet: {err}. Check the tasks in README.md")


if __name__ == "__main__":
    main()
