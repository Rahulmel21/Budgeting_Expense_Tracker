from datetime import date
from database import (
    add_budget,
    delete_budget,
    get_budget,
    get_budgets,
    get_transactions,
    update_budget,
)


def validate_budget(category, budget_limit, warning_threshold):
    if not category or category.strip() == "":
        return False, "Category cannot be empty."

    if budget_limit <= 0:
        return False, "Budget limit must be greater than zero."

    if warning_threshold < 1 or warning_threshold > 100:
        return False, "Warning threshold must be between 1 and 100."

    return True, "Budget is valid."


def create_budget(user_id, category, budget_limit, warning_threshold=80):
    valid, message = validate_budget(category, budget_limit, warning_threshold)
    if not valid:
        return False, message

    budget_id = add_budget(user_id, category.strip(), budget_limit, warning_threshold)
    if budget_id is not None:
        return True, "Budget created successfully."

    return False, "Could not create the budget."


def view_budgets(user_id):
    return get_budgets(user_id)


def view_budget(budget_id, user_id):
    return get_budget(budget_id, user_id)


def edit_budget(budget_id, user_id, budget_limit, warning_threshold=80):
    budget = get_budget(budget_id, user_id)
    if budget is None:
        return False, "Budget not found."

    category = budget["category"]
    valid, message = validate_budget(category, budget_limit, warning_threshold)
    if not valid:
        return False, message

    result = update_budget(budget_id, user_id, budget_limit, warning_threshold)
    if result:
        return True, "Budget updated successfully."

    return False, "Could not update the budget."


def remove_budget(budget_id, user_id):
    result = delete_budget(budget_id, user_id)
    if result:
        return True, "Budget deleted successfully."

    return False, "Budget not found or could not be deleted."


def calculate_monthly_spending(user_id, category, month=None):
    if month is None:
        month = date.today().strftime("%Y-%m")

    transactions = get_transactions(user_id)
    total_spending = 0

    for transaction in transactions:
        if transaction.get("transactionType") != "expense":
            continue

        if transaction.get("category", "").lower() != category.lower():
            continue

        tx_date = str(transaction.get("date", ""))
        if tx_date.startswith(month):
            total_spending += float(transaction.get("amount", 0))

    return total_spending


def check_budget_status(user_id, budget_id, month=None):
    budget = get_budget(budget_id, user_id)
    if budget is None:
        return None, "Budget not found."

    category = budget["category"]
    budget_limit = float(budget["budgetLimit"])
    warning_threshold = float(budget["warningThreshold"])

    spending = calculate_monthly_spending(user_id, category, month)
    percentage_used = (spending / budget_limit) * 100 if budget_limit > 0 else 0
    remaining = budget_limit - spending

    if spending > budget_limit:
        message = "Alert: You have exceeded your budget."
    elif percentage_used >= warning_threshold:
        message = "Warning: You are approaching your budget limit."
    else:
        message = "Your spending is within the budget limit."

    status = {
        "category": category,
        "budget_limit": budget_limit,
        "total_spending": round(spending, 2),
        "remaining_budget": round(remaining, 2),
        "percentage_used": round(percentage_used, 2),
        "warning_threshold": warning_threshold,
        "month": month if month is not None else date.today().strftime("%Y-%m"),
    }

    return status, message


def check_all_budgets(user_id, month=None):
    budgets = get_budgets(user_id)
    results = []

    for budget in budgets:
        status, message = check_budget_status(user_id, budget["budgetID"], month)
        if status is not None:
            status["message"] = message
            results.append(status)

    return results