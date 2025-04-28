import uuid
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from loguru import logger

from routes import router
from config import general_settings
from log import configure_logs


SECRET_KEY = general_settings.AUTH_SECRET
ALGORITHM = general_settings.AUTH_ALGORITHM

configure_logs()

app = FastAPI(
    title="Utils Features API",
    description="An schema for utils features",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_logging_context(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    name = None
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[-1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            name = payload.get("name")
        except JWTError:
            name = None
    with logger.contextualize(request_id=request_id, name=name):
        response = await call_next(request)

    return response


app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
