from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = (
            f"Client: {request.client.host}:{request.client.port} | "
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Completed in {processing_time:.2f}s"
        )

        print(message)
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )

    # app.add_middleware(
    #     TrustedHostMiddleware,
    #     allowed_host=[""]
    # )
