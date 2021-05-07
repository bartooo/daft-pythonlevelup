from fastapi import APIRouter, Response, status
import sqlite3

from fastapi.exceptions import HTTPException

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


@router.get("/products/{id}")
def get_product_by_id(response: Response):
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
