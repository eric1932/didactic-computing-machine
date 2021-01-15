import os

from fastapi import FastAPI

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


@app.get("/{item}")
async def call(item: str):
    exist = (item + ".py") in os.listdir("./jobs") and item != "example"
    if not exist:
        return {"status": "failure",
                "code": "Not-Exist"}

    instance = Wrapper.get_instance(item)
    return instance.call()
