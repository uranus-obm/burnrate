from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database setup ──────────────────────────────
DATABASE_URL = "sqlite:///expenses.db"
engine = create_engine(DATABASE_URL)

# ── This is your table ──────────────────────────
# Every field here = one column in the database
class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    date: date
    category: str
    notes: Optional[str] = None

# ── Create tables on startup ────────────────────
@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)

# ── CREATE ──────────────────────────────────────
@app.post("/expenses")
def add_expense(expense: Expense):
    with Session(engine) as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense

# ── READ ALL ────────────────────────────────────
@app.get("/expenses")
def get_expenses():
    with Session(engine) as session:
        return session.exec(select(Expense)).all()

# ── READ ONE ────────────────────────────────────
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense

# ── UPDATE ──────────────────────────────────────
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated: Expense):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        expense.title    = updated.title
        expense.amount   = updated.amount
        expense.date     = updated.date
        expense.category = updated.category
        expense.notes    = updated.notes
        session.commit()
        session.refresh(expense)
        return expense

# ── DELETE ──────────────────────────────────────
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        session.delete(expense)
        session.commit()
        return {"message": "Deleted successfully"}
