from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from db import schemas, models, crud
from db.db import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    return crud.get_suppliers(db)
