import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from feedback.models.response import Annotation
from supertokens_python import init, InputAppInfo, SupertokensConfig, get_all_cors_headers
from supertokens_python.recipe import emailpassword, session
from supertokens_python.framework.fastapi import get_middleware
import os
from dotenv import load_dotenv

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

LOGGER = logging.getLogger("uvicorn")


def _validate_docx(file: UploadFile) -> None:
    if not file.filename or not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=400, detail=f"{file.filename} is not a .docx file"
        )
    LOGGER.info(f"Received: {file.filename}")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    LOGGER.info("Feedback service started. Loading model.")
    yield
    LOGGER.info("Feedback quality service shutting down.")


app = FastAPI(
    title="Feedback Service",
    lifespan=_lifespan,
)

app.add_middleware(get_middleware())
# app.add_middleware(TrustedHostMiddleware)
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


@app.post("/ingest")
async def ingest(
    good: list[UploadFile] = File(...),  # noqa: B008
    marked: list[UploadFile] = File(...),  # noqa: B008
    module_context: str = Form(...),  # noqa: B008
) -> Response:
    for file in good + marked:
        _validate_docx(file)
    return Response(status_code=200)


@app.post("/check", response_model=list[Annotation])
async def check(
    file: UploadFile = File(...),  # noqa: B008
) -> list[Annotation]:
    _validate_docx(file)
    return [
        Annotation(
            span="The play ends happily.",
            comment="Oversimplified. Resolution is more ambiguous than stated.",
        ),
    ]