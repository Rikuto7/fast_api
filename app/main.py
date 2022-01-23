from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import test, user, post


def get_application():
    app = FastAPI(title="app")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(test.router, prefix="/test")
    app.include_router(user.router, prefix="/user")
    app.include_router(post.router, prefix="/post")

    return app

app = get_application()


@app.get('/')
async def root():
    return {'message': 'Hello World'}