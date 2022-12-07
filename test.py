from io import BytesIO
from aiohttp import ClientSession
import base64
import asyncio
import json

url = "https://wise-rings-rescue-35-227-151-67.loca.lt/"


async def main():
    payload = {
        "text": "test",
        "num_images": 1,
    }
    async with ClientSession() as session:
        async with session.post(url + "dalle", json=payload) as response:
            data_uri = json.loads(await response.text())["generatedImgs"][0]

    if len(data_uri) < 500:
        return data_uri

    image = BytesIO(base64.b64decode(data_uri))

    with open("craiyon.jpg", "wb") as f:
        f.write(image.getbuffer())

asyncio.run(main())
