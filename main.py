from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

expenses = []
next_id = 1

class Expense(BaseModel):
    title: str
    amount: float
    date: date
    category: str
    notes: Optional[str] = None

@app.post("/expenses")
def add_expense(expense: Expense):
    global next_id
    new_expense = expense.model_dump()
    new_expense["id"] = next_id
    expenses.append(new_expense)
    next_id += 1
    return new_expense

@app.get("/expenses")
def get_expenses():
    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            expenses.pop(i)
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense not found")
