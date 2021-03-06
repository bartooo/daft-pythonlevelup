from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from db import models, schemas


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


def get_products_by_supplier_id(db: Session, supplier_id: int):
    return (
        db.query(
            models.Product.ProductName,
            models.Product.ProductID,
            models.Category.CategoryID,
            models.Category.CategoryName,
            models.Product.Discontinued,
        )
        .join(models.Supplier, models.Supplier.SupplierID == models.Product.SupplierID)
        .join(models.Category, models.Category.CategoryID == models.Product.CategoryID)
        .filter(models.Product.SupplierID == supplier_id)
        .order_by(models.Product.ProductID.desc())
        .all()
    )


def get_category_by_id(db: Session, category_id: int):
    return (
        db.query(models.Category)
        .filter(models.Category.CategoryID == category_id)
        .first()
    )


def insert_supplier(db: Session, new_supplier: models.Supplier):
    if not new_supplier.SupplierID:
        new_supplier.SupplierID = (
            db.query(func.max(models.Supplier.SupplierID)).first()[0] + 1
        )
    db.add(new_supplier)
    db.commit()
    return new_supplier.SupplierID


def update_supplier(db: Session, id: int, to_update: schemas.Supplier):
    update_dict = {k: v for k, v in dict(to_update).items() if v is not None}
    if update_dict:
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update(
            update_dict
        )
        db.commit()


def delete_supplier(db: Session, id: int):
    db.query(models.Supplier).filter(models.Supplier.SupplierID == id).delete()
    db.commit()
