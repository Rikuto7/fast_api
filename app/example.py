from fastapi import (
    FastAPI, APIRouter, HTTPException, Depends, status,
    Body, Query, Path, File, UploadFile, Header, Cookie,
    Form, BackgroundTasks
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

from starlette.exceptions import HTTPException as StarletteHTTPException

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, Dict, List, Set