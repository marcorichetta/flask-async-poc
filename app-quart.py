from quart import Quart

app = Quart(__name__)

import asyncio


@app.route("/")
async def hello_world():
    await asyncio.sleep(0.25)
    return "Hello, World!"
