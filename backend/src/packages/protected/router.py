import time

from fastapi import APIRouter, Depends, Request, Response
from loguru import logger
from packages.auth import get_current_user
from utils.responses import InternalServerErrorResponse

from .responses import Product, ProductList, ProductListOut


protected_router = APIRouter()

fake_products_db = [
    {
        "id": 1,
        "name": "Product 1",
        "description": "Description of Product 1",
        "price": 10.0,
    },
    {
        "id": 2,
        "name": "Product 2",
        "description": "Description of Product 2",
        "price": 20.0,
    },
]


@protected_router.get(
    "",
    responses={
        200: {"model": ProductListOut},
        500: {"model": InternalServerErrorResponse},
    },
)
async def get_products(
    request: Request,
    response: Response,
    current_user: str = Depends(get_current_user),
):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Fetching products by user {current_user}")

        process_time = time.time() - start_time

        logger.info(f"Fetched products in {process_time:.2f} seconds")
        new_products = [Product(**product) for product in fake_products_db]
        product_list = ProductList(
            items=new_products, total=len(fake_products_db)
        )

        logger.info(f"Product list: {product_list}")

        return ProductListOut(
            request_id=request_id,
            process_time=process_time,
            message="Products fetched successfully",
            payload=product_list,
        )
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        response.status_code = 500
        return {
            "request_id": request_id,
            "process_time": 0,
            "message": "Internal Server Error",
            "func": "get_products",
        }
