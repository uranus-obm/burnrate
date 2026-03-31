import os
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://uranus-obm.github.io",
        "https://featured-numeric-quilt-proven.trycloudflare.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = "sqlite:///./expenses.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}  
)

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    date: date
    category: str
    notes: Optional[str] = None

# Create DB tables
@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)

# Routes
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Burnrate Backend is Running",
        "port": 6767,
        "endpoints": ["/expenses", "/docs"]
    }

@app.post("/expenses")
def add_expense(expense: Expense):
    with Session(engine) as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense

@app.get("/expenses")
def get_expenses():
    with Session(engine) as session:
        return session.exec(select(Expense)).all()

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated: Expense):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        expense_data = updated.model_dump(exclude_unset=True)
        for key, value in expense_data.items():
            setattr(expense, key, value)

        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        session.delete(expense)
        session.commit()
        return {"message": "Deleted successfully"}
