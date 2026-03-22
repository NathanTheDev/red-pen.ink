# ruff: noqa: B008

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from refactor.feedback.routers.check import router as check_router
from refactor.feedback.routers.injest import router as injest_router
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import emailpassword, session

load_dotenv()
init(
    app_info=InputAppInfo(
        app_name="red.ink",
        api_domain="http://localhost:8080",
        website_domain="http://localhost:3001",
        api_base_path="/auth",
        website_base_path="/login",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri=os.environ["SUPERTOKENS_CONNECTION_URI"],
        api_key=os.environ["SUPERTOKENS_API_KEY"],
    ),
    framework="fastapi",
    recipe_list=[
        emailpassword.init(),
        session.init(),
    ],
    mode="asgi",
)
logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    logger.info("Feedback service started. Loading model.")
    yield
    logger.info("Feedback quality service shutting down.")


app = FastAPI(
    title="Feedback Service",
    lifespan=_lifespan,
)

app.add_middleware(get_middleware())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)


@app.get("/", include_in_schema=False)
@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(injest_router)
app.include_router(check_router)
