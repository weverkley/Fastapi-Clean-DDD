import os
import time
import uvicorn
from asyncio.log import logger
from fastapi.responses import JSONResponse
from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from src.domain.exception.permission_denied_exception import PermissionDeniedException
from src.infrastructure.ioc.mappings import configure_mappings
from src.presentation.api.v1 import auth_routes
from src.presentation.api.v1 import user_routes

app = FastAPI(
    title="API Clean/DDD architecture using imperative mapping",
    version="1.0.0",
    description="An example of how to implement DDD, Clean Architecture and JWT validation middleware in FastAPI."
)
internal_router = APIRouter()

configure_mappings()
internal_router.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
internal_router.include_router(user_routes.router, prefix="/users", tags=["Users"])

app.include_router(internal_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def global_error_handler_middleware(request: Request, call_next):
    """
    This middleware catches any unhandled exception that occurs during request processing
    and returns a standardized JSON error response.
    """
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except PermissionDeniedException as e:
        logger.warning(f"Permission denied for request {request.method} {request.url}: {e}")

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": "Permission Denied",
                "message": str(e),
                "timestamp": time.time(),
            },
        )
    except HTTPException as e:
         raise e

    except Exception as e:
        logger.exception(f"Unhandled error for request {request.method} {request.url}: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later.",
                "timestamp": time.time()
            },
        )

if __name__ == "__main__":
    if os.getenv("APP_ENV") == "production":
        uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info", workers=1)
    elif os.getenv("APP_ENV") == "development":
        uvicorn.run(
            "main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
        )
