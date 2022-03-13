import os
import pathlib
from fastapi import APIRouter, Response, status, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from api.schemas import schemas


router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM = os.environ.get('MAIL_FROM'),
    MAIL_FROM_NAME=os.environ.get('MAIL_FROM_NAME'),
    MAIL_PORT = os.environ.get('MAIL_PORT'),
    MAIL_SERVER = os.environ.get('MAIL_SERVER'),
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER = str(pathlib.Path(__file__).resolve().parent.parent.parent / "templates/email")
)

html = """
<p>Hi this test mail, thanks for using Fastapi-mail</p>
"""


@router.post('/send')
async def send_mail(email: schemas.EmailSchema):
    message = MessageSchema(
        subject="Fastapi-Mail",
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')

    Response(status_code=status.HTTP_200_OK)


@router.post('/send_background')
def send_mail_background(background_tasks: BackgroundTasks, email: schemas.EmailSchema):
    message = MessageSchema(
        subject="Fastapi-Background-Mail",
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
        subtype="html"
    )
    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name='email.html'
    )

    Response(status_code=status.HTTP_200_OK)