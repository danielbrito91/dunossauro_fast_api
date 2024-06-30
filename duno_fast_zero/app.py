from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root():
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
