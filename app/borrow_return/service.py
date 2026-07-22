from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.borrow_return.models import BorrowTransaction
from app.models.inventory import Inventory


def borrow_component(data, db: Session):

    component = db.query(Inventory).filter(
        Inventory.component_id == data.component_id
    ).first()

    if component is None:
        raise HTTPException(
            status_code=404,
            detail="Component Not Found"
        )

    if component.quantity < data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient Stock"
        )

    component.quantity -= data.quantity

    transaction = BorrowTransaction(
        student_id=data.student_id,
        component_id=data.component_id,
        quantity=data.quantity,
        borrow_time=datetime.now()
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)

    return transaction


def return_component(data, db: Session):

    transaction = db.query(BorrowTransaction).filter(
        BorrowTransaction.transaction_id == data.transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction Not Found"
        )

    component = db.query(Inventory).filter(
        Inventory.component_id == transaction.component_id
    ).first()

    component.quantity += transaction.quantity

    transaction.return_time = datetime.now()

    transaction.status = "RETURNED"

    db.commit()

    db.refresh(transaction)

    return transaction