from fastapi import APIRouter, Response, status
import sqlite3
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.params import Query
from fastapi.responses import JSONResponse

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = sqlite3.connect("northwind.db", check_same_thread=False)
    router.db_connection.text_factory = lambda b: b.decode(
        errors="ignore"
    )  # northwind specific


@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get("/categories")
async def get_categories(response: Response):
    response.status_code = status.HTTP_200_OK
    router.db_connection.row_factory = sqlite3.Row
    data = router.db_connection.execute(
        "SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID"
    ).fetchall()
    return {
        "categories": [{"id": x["CategoryID"], "name": x["CategoryName"]} for x in data]
    }


@router.get("/customers")
async def get_categories(response: Response):
    response.status_code = status.HTTP_200_OK
    router.db_connection.row_factory = sqlite3.Row
    data = router.db_connection.execute(
        "SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers"
    ).fetchall()
    return {
        "customers": [
            {
                "id": x["CustomerID"],
                "name": x["CompanyName"],
                "full_address": f'{x["Address"]} {x["PostalCode"]} {x["City"]} {x["Country"]}',
            }
            for x in data
        ]
    }


@router.get("/products/{id}", response_class=JSONResponse)
async def get_product_by_id(response: Response, id: int):
    router.db_connection.row_factory = sqlite3.Row
    data = router.db_connection.execute(
        "SELECT ProductName FROM Products WHERE ProductID = :product_id",
        {"product_id": id},
    ).fetchone()
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record with given id not found",
        )
    response.status_code = status.HTTP_200_OK
    return {"id": id, "name": data["ProductName"]}


def check_order(order):
    if order not in {"first_name", "last_name", "city", "EmployeeID"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong order parameter",
        )


@router.get("/employees", response_class=JSONResponse)
async def get_employees(
    response: Response,
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    order: Optional[str] = Query("EmployeeID"),
):
    response.status_code = status.HTTP_200_OK
    check_order(order)
    order = "".join([word.capitalize() for word in order.split("_")])
    router.db_connection.row_factory = sqlite3.Row
    query = f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY {order} ASC"
    if limit:
        query += f" LIMIT {limit}"
    if offset:
        query += f" OFFSET {offset}"
    data = router.db_connection.execute(query).fetchall()
    return {
        "employees": [
            {
                "id": x["EmployeeID"],
                "last_name": x["LastName"],
                "first_name": x["FirstName"],
                "city": x["City"],
            }
            for x in data
        ]
    }


@router.get("/products_extended")
async def products_extended(response: Response):
    response.status_code = status.HTTP_200_OK
    router.db_connection.row_factory = sqlite3.Row
    data = router.db_connection.execute(
        "SELECT ProductID, ProductName, CategoryName, CompanyName FROM Products JOIN Categories ON Products.CategoryID = Categories.CategoryID JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID"
    )
    return {
        "products_extended": [
            {
                "id": x["ProductID"],
                "name": x["ProductName"],
                "category": x["CategoryName"],
                "supplier": x["CompanyName"],
            }
            for x in data
        ]
    }


def check_if_product_exists(id: int):
    router.db_connection.row_factory = sqlite3.Row
    data = router.db_connection.execute(
        "SELECT ProductID FROM Products WHERE ProductID = :product_id",
        {"product_id": id},
    ).fetchone()
    return False if data is None else True


@router.get("/products/{id}/orders")
async def get_orders_by_product_id(response: Response, id: int):
    response.status_code = status.HTTP_200_OK
    if not check_if_product_exists(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record with given id not found",
        )
    data = router.db_connection.execute(
        "SELECT Products.ProductID, Orders.OrderID, Customers.CompanyName, 'Order Details'.Quantity, ROUND(('Order Details'.UnitPrice * 'Order Details'.Quantity) - ('Order Details'.Discount * ('Order Details'.UnitPrice * 'Order Details'.Quantity)), 2) AS TotalPrice FROM Products JOIN 'Order Details' ON Products.ProductID = 'Order Details'.ProductID JOIN Orders ON 'Order Details'.OrderID = Orders.OrderID JOIN Customers ON Orders.CustomerID = Customers.CustomerID WHERE ProductID = :product_id",
        {"product_id": id},
    ).fetchall()
    return {
        "orders": [
            {
                "id": x["OrderID"],
                "customer": x["CompanyName"],
                "quantity": x["Quantity"],
                "total_price": x["TotalPrice"],
            }
            for x in data
        ]
    }
