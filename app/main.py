import logging

from fastapi import FastAPI, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.routers import (test, user, post, profile, connection, mail, chat)


def get_application():
    app = FastAPI(title="app", debug=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(test.router, prefix="/test", tags=["test"])
    app.include_router(user.router, prefix="/user", tags=["user"])
    app.include_router(post.router, prefix="/post", tags=["post"])
    app.include_router(profile.router, prefix="/profile", tags=["profile"])
    app.include_router(connection.router, prefix="/connection", tags=["connection"])
    app.include_router(mail.router, prefix="/mail", tags=["mail"])
    app.include_router(chat.router, prefix="/chat", tags=["chat"])

    return app

app = get_application()
add_pagination(app)


@app.get('/')
async def root():
    return {'message': 'Index'}
