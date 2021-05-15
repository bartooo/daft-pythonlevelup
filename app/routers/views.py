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


@router.get("/suppliers", response_model=List[schemas.SupplierTmp])
async def get_suppliers(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    return crud.get_suppliers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers/{supplier_id}/products")
async def get_products_by_supplier_id(supplier_id: int, db: Session = Depends(get_db)):
    db_products = crud.get_products_by_supplier_id(db, supplier_id)
    if not db_products or db_products[0].ProductID is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return [
        {
            "ProductID": row.ProductID,
            "ProductName": row.ProductName,
            "Category": {
                "CategoryID": row.CategoryID,
                "CategoryName": row.CategoryName,
            },
            "Discontinued": row.Discontinued,
        }
        for row in db_products
    ]
