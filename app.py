from flask import Flask

app = Flask(__name__)

import asyncio


@app.route("/")
async def hello_world():
    await asyncio.sleep(0.25)
    return "Hello, World!"
