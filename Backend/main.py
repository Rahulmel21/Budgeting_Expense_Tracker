from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from database import get_total_income, get_total_expenses, get_balance
from authentication import register_user, login_user
from transaction import create_transaction, view_transactions, remove_transaction
from budgeting import create_budget, view_budgets, check_budget_status, remove_budget
from reports import calculate_report_summary, export_transactions_to_csv, export_summary_to_csv

app = FastAPI()

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TransactionRequest(BaseModel):
    amount: float
    transaction_type: str
    category: str
    date: str
    payment_method: str
    notes: Optional[str] = ""

class BudgetRequest(BaseModel):
    category: str
    budget_limit: float
    warning_threshold: int = 80

class ReportRequest(BaseModel):
    start_date: str
    end_date: str

def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    try:
        return int(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def api_register(data: RegisterRequest):
    success, msg = register_user(data.username, data.password, data.email)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@app.post("/login")
def api_login(data: LoginRequest):
    success, result = login_user(data.username, data.password)
    if not success:
        raise HTTPException(status_code=401, detail=result)
    return {"access_token": str(result), "user_id": result}

@app.get("/dashboard")
def api_dashboard(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    return {
        "total_income": get_total_income(user_id),
        "total_expenses": get_total_expenses(user_id),
        "balance": get_balance(user_id),
    }

@app.get("/transactions")
def api_get_transactions(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    return view_transactions(user_id)

@app.post("/transactions")
def api_add_transaction(data: TransactionRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    success, msg = create_transaction(
        user_id, data.amount, data.transaction_type,
        data.category, data.date, data.payment_method, data.notes
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@app.delete("/transactions/{transaction_id}")
def api_delete_transaction(transaction_id: int, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    success, msg = remove_transaction(transaction_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=msg)
    return {"message": msg}

@app.get("/budgets")
def api_get_budgets(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    return view_budgets(user_id)

@app.post("/budgets")
def api_add_budget(data: BudgetRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    success, msg = create_budget(user_id, data.category, data.budget_limit, data.warning_threshold)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@app.get("/budgets/{budget_id}/status")
def api_budget_status(budget_id: int, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    status, msg = check_budget_status(user_id, budget_id)
    if status is None:
        raise HTTPException(status_code=404, detail=msg)
    return {"budget_status": status, "message": msg}

@app.delete("/budgets/{budget_id}")
def api_delete_budget(budget_id: int, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    success, msg = remove_budget(budget_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=msg)
    return {"message": msg}

@app.post("/reports/summary")
def api_report_summary(data: ReportRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    summary, msg = calculate_report_summary(user_id, data.start_date, data.end_date)
    if summary is None:
        raise HTTPException(status_code=400, detail=msg)
    return {"report": summary, "message": msg}

@app.post("/reports/export/transactions")
def api_export_transactions(data: ReportRequest, background_tasks: BackgroundTasks, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    filename = f"transactions_{user_id}.csv"
    success, msg = export_transactions_to_csv(user_id, data.start_date, data.end_date, filename)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    background_tasks.add_task(os.remove, filename)
    return FileResponse(filename, media_type="text/csv", filename="transaction_report.csv")

@app.post("/reports/export/summary")
def api_export_summary(data: ReportRequest, background_tasks: BackgroundTasks, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    filename = f"summary_{user_id}.csv"
    success, msg = export_summary_to_csv(user_id, data.start_date, data.end_date, filename)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    background_tasks.add_task(os.remove, filename)
    return FileResponse(filename, media_type="text/csv", filename="summary_report.csv")