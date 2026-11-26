# transactions.py

# Import transaction functions from database.py
from database import add_transaction
from database import get_transactions
from database import get_transaction
from database import update_transaction
from database import delete_transaction
from database import search_transactions


# --------------------------------------------------
# FUNCTION 1: Validate Transaction
# --------------------------------------------------

def validate_transaction(amount, transaction_type, category,
                         date, payment_method, notes=""):

    # Check whether amount is positive
    if amount <= 0:
        return False, "Amount must be greater than zero."

    # Check transaction type
    if transaction_type not in ["income", "expense"]:
        return False, "Type must be income or expense."

    # Check category
    if category.strip() == "":
        return False, "Category cannot be empty."

    # Check date
    if date.strip() == "":
        return False, "Date cannot be empty."

    # Check payment method
    if payment_method.strip() == "":
        return False, "Payment method cannot be empty."

    # All validation checks passed
    return True, "Transaction is valid."


# --------------------------------------------------
# FUNCTION 2: Add Transaction
# --------------------------------------------------

def create_transaction(user_id, amount, transaction_type,
                       category, date, payment_method, notes=""):

    # Validate transaction information
    valid, message = validate_transaction(
        amount, transaction_type, category,
        date, payment_method, notes
    )

    # Stop if validation fails
    if not valid:
        return False, message

    # Save transaction in the database
    transaction_id = add_transaction(
        user_id, amount, transaction_type,
        category, date, payment_method, notes
    )

    # Return the result
    if transaction_id is not None:
        return True, "Transaction added successfully."

    return False, "Could not add transaction."


# --------------------------------------------------
# FUNCTION 3: View All Transactions
# --------------------------------------------------

def view_transactions(user_id):

    # Retrieve transactions belonging to this user
    return get_transactions(user_id)


# --------------------------------------------------
# FUNCTION 4: View One Transaction
# --------------------------------------------------

def view_transaction(transaction_id, user_id):

    # Retrieve one transaction belonging to this user
    return get_transaction(transaction_id, user_id)


# --------------------------------------------------
# FUNCTION 5: Edit Transaction
# --------------------------------------------------

def edit_transaction(transaction_id, user_id,
                     amount, transaction_type,
                     category, date, payment_method, notes=""):

    # Check the new transaction details
    valid, message = validate_transaction(
        amount, transaction_type, category,
        date, payment_method, notes
    )

    if not valid:
        return False, message

    # Update the transaction in the database
    result = update_transaction(
        transaction_id, user_id, amount,
        transaction_type, category, date,
        payment_method, notes
    )

    if result:
        return True, "Transaction updated successfully."

    return False, "Transaction not found or update failed."


# --------------------------------------------------
# FUNCTION 6: Delete Transaction
# --------------------------------------------------

def remove_transaction(transaction_id, user_id):

    # Delete only the specified user's transaction
    result = delete_transaction(transaction_id, user_id)

    if result:
        return True, "Transaction deleted successfully."

    return False, "Transaction not found or deletion failed."


# --------------------------------------------------
# FUNCTION 7: Search Transactions
# --------------------------------------------------

def search_user_transactions(user_id, keyword):

    # Check whether the search keyword is empty
    if keyword.strip() == "":
        return [], "Please enter a search keyword."

    # Search the database
    results = search_transactions(user_id, keyword)

    return results, "Search completed successfully."


# --------------------------------------------------
# FUNCTION 8: Filter Transactions
# --------------------------------------------------

def filter_transactions(user_id,
                        transaction_type=None,
                        category=None,
                        start_date=None,
                        end_date=None):

    # Get all transactions belonging to the user
    transactions = get_transactions(user_id)

    # Create an empty list for matching transactions
    filtered_transactions = []

    # Examine each transaction
    for transaction in transactions:

        # Filter by income or expense
        if transaction_type is not None:
            if transaction["transactionType"] != transaction_type:
                continue

        # Filter by category
        if category is not None:
            if transaction["category"] != category:
                continue

        # Filter by starting date
        if start_date is not None:
            if transaction["date"] < start_date:
                continue

        # Filter by ending date
        if end_date is not None:
            if transaction["date"] > end_date:
                continue

        # Add matching transaction to the result
        filtered_transactions.append(transaction)

    return filtered_transactions