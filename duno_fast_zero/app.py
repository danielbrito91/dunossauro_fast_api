from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from duno_fast_zero.routers import auth, users
from duno_fast_zero.schemas import (
    Message,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá, galera!'}


@app.get('/ex01', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def ex_01():
    html_content = """<html>
        <head>
            <title>FastAPI</title>
        </head>
        <body>
            <h1>olá mundo!</h1>
        </body>
    </html>
            """
    return html_content
