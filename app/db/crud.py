from sqlalchemy.orm import Session, load_only

from db import models


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return (
        db.query(models.Supplier.SupplierID, models.Supplier.CompanyName)
        .order_by(models.Supplier.SupplierID.asc())
        .all()
    )


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier)
        .filter(models.Supplier.SupplierID == supplier_id)
        .first()
    )
