from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(String, nullable=True)
Base.metadata.create_all(bind=engine)
class ExpenseCreate(BaseModel):
    title: str = Field(..., example="Food")
    amount: float = Field(..., gt=0)  # iff > 0
    date: date
    category: str
    notes: Optional[str] = None
class ExpenseUpdate(BaseModel):
    title: Optional[str]
    amount: Optional[float]
    date: Optional[date]
    category: Optional[str]
    notes: Optional[str]
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    date: date
    category: str
    notes: Optional[str]
    class Config:
        from_attributes = True  # convert
app = FastAPI(title="Expense Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/expenses", response_model=ExpenseResponse)
def add_expense(expense: ExpenseCreate):
    db = SessionLocal()
    new_expense = ExpenseDB(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)  

    db.close()
    return new_expense
@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(10, le=100),
    offset: int = 0
):
    db = SessionLocal()
    query = db.query(ExpenseDB)
    if category:
        query = query.filter(ExpenseDB.category == category)
    if start_date:
        query = query.filter(ExpenseDB.date >= start_date)
    if end_date:
        query = query.filter(ExpenseDB.date <= end_date)
    expenses = query.offset(offset).limit(limit).all()
    db.close()
    return expenses
@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    db = SessionLocal()
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not expense:
        db.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    db.close()
    return expense
@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, updated_data: ExpenseUpdate):
    db = SessionLocal()
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not expense:
        db.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    db.close()
    return expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    db = SessionLocal()
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not expense:
        db.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    db.close()
    return {"message": "Deleted"}
# she say do u love me i tell her only partly, i only love my mama, my bed i am sorry
