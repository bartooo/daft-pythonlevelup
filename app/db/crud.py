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
    db.add(new_supplier)
    # db.flush()
    # new_id = new_supplier.SupplierID
    db.commit()
    # return new_id
