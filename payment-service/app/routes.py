from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import Payment, Transaction
from app.schemas import PaymentCreate, PaymentRead, TransactionCreate, TransactionRead
from app.database import get_session

router = APIRouter()

# Create a new payment
@router.post("/payments/", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, session: Session = Depends(get_session)):
    new_payment = Payment(**payment.dict(), status="pending")
    session.add(new_payment)
    session.commit()
    session.refresh(new_payment)
    return new_payment

# Read a specific payment by ID
@router.get("/payments/{payment_id}", response_model=PaymentRead)
def read_payment(payment_id: int, session: Session = Depends(get_session)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Create a new transaction
@router.post("/transactions/", response_model=TransactionRead)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)):
    new_transaction = Transaction(**transaction.dict(), status="completed")
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    return new_transaction

# Read a specific transaction by ID
@router.get("/transactions/{transaction_id}", response_model=TransactionRead)
def read_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Example route to show usage of select for more complex queries
@router.get("/payments/pending/", response_model=list[PaymentRead])
def read_pending_payments(session: Session = Depends(get_session)):
    # Example of using select to get all pending payments
    statement = select(Payment).where(Payment.status == "pending")
    results = session.exec(statement).all()
    return results