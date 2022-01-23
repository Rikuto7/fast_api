from typing import List
from fastapi import APIRouter


router = APIRouter()

@router.get("/")
async def get_all_test() -> List[dict]:
    test = [
        {'msg': 'test'}
    ]

    return test
