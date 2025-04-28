import time

from loguru import logger
from fastapi import APIRouter, Request, Response
from utils.responses import (
    SuccessResponse,
    ConflictResponse,
    NotFoundResponse,
    InternalServerErrorResponse,
)

from .responses import TokenOut
from .config import auth_settings
from .schemas import LoginInfo, CreateInfo
from .utils import (
    authenticate_user,
    create_access_token,
    fake_users_db,
    get_password_hash,
)

auth_router = APIRouter()

EXPIRE_MINUTES = auth_settings.EXPIRE_MINUTES


@auth_router.post(
    "/login",
    responses={
        200: {"model": TokenOut},
        401: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
async def login(request: Request, response: Response, login_input: LoginInfo):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Logging in {login_input.email}")

        valid_user = authenticate_user(login_input.email, login_input.password)

        if not valid_user:
            logger.warning(f"Error logging in: {login_input.email}")
            response.status_code = 401
            return NotFoundResponse(
                request_id=request_id,
                process_time=0,
                message="Invalid credentials",
                func="login",
            )

        token = create_access_token(
            data={
                "email": valid_user["email"],
                "name": valid_user["name"],
            },
        )

        process_time = time.time() - start_time

        logger.info(f"Logged in in {process_time:.2f} seconds")
        return TokenOut(
            request_id=request_id,
            process_time=process_time,
            func="login",
            message="User logged in",
            payload=token,
        )
    except Exception as e:
        logger.error(f"Error logging in: {e}")
        response.status_code = 500
        return InternalServerErrorResponse(
            request_id=request_id, message=str(e), func="login"
        )


@auth_router.post(
    "/register",
    responses={
        200: {"model": SuccessResponse},
        409: {"model": InternalServerErrorResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
async def register(
    register_info: CreateInfo, request: Request, response: Response
):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Registering {register_info.name}")

        if register_info.email in fake_users_db:
            logger.warning(f"Error registering: {register_info.email}")
            response.status_code = 409
            return ConflictResponse(
                request_id=request_id,
                process_time=0,
                message="User already exists",
                func="register",
            )

        fake_users_db[register_info.email] = {
            "email": register_info.email,
            "name": register_info.name,
            "hashed_password": get_password_hash(register_info.password),
        }
        process_time = time.time() - start_time

        logger.info(f"Registered in {process_time:.2f} seconds")
        return SuccessResponse(
            request_id=request_id,
            process_time=process_time,
            func="register",
            message="User registered",
        )
    except Exception as e:
        logger.error(f"Error registering: {e}")
        return InternalServerErrorResponse(
            request_id=request_id, message=str(e), func="register"
        )
