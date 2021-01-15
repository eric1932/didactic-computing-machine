import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from wrapper import Wrapper

if not os.path.exists("./logs"):
    os.mkdir("./logs")

app = FastAPI()


def exec_get_value(item):
    _l = locals()
    exec(f"t = {item}", globals(), _l)
    return _l["t"]


@app.get("/")
def root():
    return {"Title": "Hello World!"}


@app.get("/sign/{item}")
async def call(item: str):
    exist = (item + ".py") in os.listdir("./jobs") and item != "example"
    if not exist:
        return {"status": "failure",
                "code": "Not-Exist"}

    instance = Wrapper.get_instance(item)
    return instance.call()


@app.get("/list", response_class=HTMLResponse)
def list_jobs():
    html_template = """
    <html>
        <head>
            <title>All Jobs</title>
        </head>
        <body>
            <HTML_BODY>
        </body>
    </html>
    """
    html_body = ""
    for x in os.listdir("./jobs"):
        if x == "example.py" or not x.endswith(".py"):
            continue
        html_body += f"""
        <div>
            <a>{x[:-3]}</a>
        </div>
        """
    return html_template.replace("<HTML_BODY>", html_body)
