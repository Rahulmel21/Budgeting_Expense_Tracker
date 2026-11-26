import sqlite3

DB_NAME = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            passwordHash TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER NOT NULL,
            amount REAL NOT NULL,
            transactionType TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            paymentMethod TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (userID) REFERENCES users (userID)
        )
    """)
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budgetID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER NOT NULL,
            category TEXT NOT NULL,
            budgetLimit REAL NOT NULL,
            warningThreshold REAL NOT NULL,
            FOREIGN KEY (userID) REFERENCES users (userID)
        )
    """)
   
    conn.commit()
    conn.close()


def add_user(username, password_hash, email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, passwordHash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE userID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def add_transaction(user_id, amount, transaction_type, category, date, payment_method, notes):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (userID, amount, transactionType, category, date, paymentMethod, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, transaction_type, category, date, payment_method, notes),
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.Error:
        return None


def get_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM transactions WHERE userID = ? ORDER BY date DESC",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_transaction(transaction_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM transactions WHERE transactionID = ? AND userID = ?",
        (transaction_id, user_id),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_transaction(transaction_id, user_id, amount, transaction_type, category, date, payment_method, notes):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE transactions
            SET amount = ?, transactionType = ?, category = ?, date = ?, paymentMethod = ?, notes = ?
            WHERE transactionID = ? AND userID = ?
            """,
            (amount, transaction_type, category, date, payment_method, notes, transaction_id, user_id),
        )
        conn.commit()
        row_count = cursor.rowcount
        conn.close()
        return row_count > 0
    except sqlite3.Error:
        return False


def delete_transaction(transaction_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM transactions WHERE transactionID = ? AND userID = ?",
            (transaction_id, user_id),
        )
        conn.commit()
        row_count = cursor.rowcount
        conn.close()
        return row_count > 0
    except sqlite3.Error:
        return False


def search_transactions(user_id, keyword):
    conn = get_db_connection()
    cursor = conn.cursor()
    term = f"%{keyword}%"
    cursor.execute(
        """
        SELECT * FROM transactions
        WHERE userID = ? AND (category LIKE ? OR notes LIKE ? OR paymentMethod LIKE ?)
        ORDER BY date DESC
        """,
        (user_id, term, term, term),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_budget(user_id, category, budget_limit, warning_threshold):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO budgets (userID, category, budgetLimit, warningThreshold)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, category, budget_limit, warning_threshold),
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.Error:
        return None


def get_budgets(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budgets WHERE userID = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_budget(budget_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM budgets WHERE budgetID = ? AND userID = ?",
        (budget_id, user_id),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_budget(budget_id, user_id, budget_limit, warning_threshold):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE budgets
            SET budgetLimit = ?, warningThreshold = ?
            WHERE budgetID = ? AND userID = ?
            """,
            (budget_limit, warning_threshold, budget_id, user_id),
        )
        conn.commit()
        row_count = cursor.rowcount
        conn.close()
        return row_count > 0
    except sqlite3.Error:
        return False


def delete_budget(budget_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM budgets WHERE budgetID = ? AND userID = ?",
            (budget_id, user_id),
        )
        conn.commit()
        row_count = cursor.rowcount
        conn.close()
        return row_count > 0
    except sqlite3.Error:
        return False

def get_total_income(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE userID = ? AND transactionType = 'income'",
        (user_id,),
    )
    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else 0.0


def get_total_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE userID = ? AND transactionType = 'expense'",
        (user_id,),
    )
    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else 0.0


def get_balance(user_id):
    income = get_total_income(user_id)
    expenses = get_total_expenses(user_id)
    return round(income - expenses, 2)


def get_category_summary(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT category, SUM(amount) as total 
        FROM transactions 
        WHERE userID = ? AND transactionType = 'expense'
        GROUP BY category
        """,
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return {row["category"]: round(row["total"], 2) for row in rows}
init_db()