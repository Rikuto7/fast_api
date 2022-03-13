from typing import Optional
from fastapi import APIRouter, Query, Path, File, UploadFile, Depends

from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


router = APIRouter()

@router.get("/{id}")
async def get_all_test(q: Optional[str] = Query(None), id: int = Path(..., title='必須')):
    data = [
        {'q': q,
         'id': id}
    ]
    return data


@router.post("/file/")
async def create_files(
    files: bytes = File(...)
):
    print(files[0])
    print(type(files[0]))
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfile/")
async def create_upload_files(
    uploaded_file: UploadFile = File(...)
):
    file_location = f"files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
