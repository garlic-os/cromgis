from io import FileIO
from typing import Tuple
from typing import TypedDict

import asyncio
from aiohttp import ClientSession
from aiohttp.multipart import MultipartWriter
from PIL import Image
from tempfile import TemporaryFile


class S3Fields(TypedDict):
    key: str
    AWSAccessKeyId: str
    policy: str
    signature: str


TOKEN = "d29tYm8tdGhhdC1zaGl6ejpHZXRUaGF0QnJlYWQkMSE="

# User-readable dictionary of IDs of memes Wombo can make
MEMES = {
    "rickroll": 1,
    "numa-numa": 2,
    "boom": 3,
    "dreams": 4,
    "baka-mitai": 5,
    "i-feel-good": 6,
    "witch-doctor": 7,
    "everytime-we-touch": 8,
    "i-will-survive": 9,
    "dont-cha": 10,
    "tralala": 11,
    "thriller": 12,
    "bitch": 13,
    "i-will-always-love-you": 14,
    "happy-birthday": 22,
    "entertainer": 23,
    "rockin-robin": 24,
    "rising-sun": 25,
    "periodic-table": 26,
    "were-not-gonna": 31,
    "all-star": 32,
    "what-is-love": 33,
    "fortnite": 34,
    "hino-da-sociedade": 35,
    "dame-tu-cosita": 36,
    "tunak-tunak-tun": 37,
    "bande-organisee": 38,
    "ymca": 39,
    "funkytown": 40,
    "bing-bong": 41,  # premium
    "whats-going-on": 42,
    "take-on-me": 43,  # premium
    "bum-bum-tam-tam": 44,
    "i-want-it-that-way": 45,
    "blue": 46,
    "its-not-unusual": 47,  # premium
    "friday": 48,
    "trouble": 49,
    "hit-me-baby": 50,
    "happy": 51,  # premium
    "barbie": 52,
    "bidolibido": 53,
    "bum-bum-tam-tam-2": 54,  # duplicate of 44
    "miami": 55,
    "born-this-way": 56,
    "bad-guy": 57,
    "american-idiot": 58,
    "your-man": 59,
    "despacito": 60,
    "cotton-eye-joe": 61,  # premium
    "my-way": 62,
    "apna-time-aayega": 63,
    "its-raining-men": 64,
    "shake-it-off": 65,
    "chaccaron-maccaron": 66,
    "my-humps": 67,
    "milkshake": 68,  # premium
    "x-gon-give-it-to-ya": 69,
    "rasputin": 70,
    "blinding-lights": 71,
    "in-da-club": 72,  # premium
    "boombastic": 73,  # premium
    "gasolina": 74,
    "axel-f": 75,
    "bites-the-dust": 76,
    "dont-start-now": 77,
    "who-let-the-dogs-out": 78,
    "show-das-poderosas": 79,
    "pepa-no-funk": 80,
    "chaar-botal-vodka": 81,
    "nemashanmah-herati": 82,
    "because-i-got-high": 83,
    "smoke-weed-everyday": 84,
    "mary-jane": 85,
    "three-little-birds": 86,
    "2-joints": 87,
    "-": 88,  # No sound
    "have-you-ever-had-a-dream": 89,
    "heat-waves": 90,
    "tell-me-you-know": 91,
    "u-cant-touch-this": 92,  # premium
    "ko": 93,
    "la-bomba": 94,
    "rowdy-baby": 95,
    "tujhe-dekha-to": 96,
    "watskeburt": 97,
    "drank-and-drugs": 98,
    "zaman": 99,
    "its-the-time-to-disco": 100,
    "heb-je-even-voor-mij": 101,
    "olha-a-explosao": 102,
    "ai-se-eu-te-pego": 103,
    "around-the-world": 104,
    "how-deep-is-your-love": 105,  # premium
    "turn-down-for-what": 106,
    "baby-got-back": 108,  # premium
    "marchas": 110,
    "wayward-son": 112,  # premium
    "drivers-license": 114,
    "get-lucky": 115,
    "gettin-jiggy-wit-it": 116,
    "girls-just-want-to-have-fun": 117,
    "hollaback-girl": 119,
    "kala-chashma": 120,
    "karma-chameleon": 121,  # premium
    "lose-yourself": 122,
    "mamma-mia": 124,  # premium
    "mans-not-hot": 125,
    "new-rules": 127,
    "pump-up-the-jam": 129,
    "run-the-world": 132,
    "sexyback": 133,
    "teen-spirit": 134,
    "tokyo-drift": 135,
    "vai-embrazando": 136,
    "we-are-the-champions": 137,
    "tommy": 139,
    "badtameez-dil": 140,
    "cafe-con-leche": 142,
    "emosanal-attyachaar": 143,
    "kabhi-kabhi-mere-dil-mein": 144,
    "kabhi-khushi-kabhie-gham": 145,
    "kal-ho-naa-ho": 146,
    "queen": 147,
    "m-to-the-b": 150,
    "pyar-hua-iqrar-hua": 150,
    "wiggle": 151,
    "womanizer": 152,
    "kokila-ben": 155,
    "sugarcrash": 156,
    "danza-kuduro": 157,
    "ilarie": 158,
    "mama": 159,
    "motherlover": 160,
    "stacys-mom": 162,
    "stewie-mum": 163,
    "im-a-cool-mom": 164,
    "xtasy": 165,
    "astronaut-in-the-ocean": 166,
    "bad-reputation": 167,
    "dromen-zijn-bedrog": 169,
    "bagagedrager": 170,
    "how-you-like-that": 171,
    "toilet": 172,  # 60fps??
    "pawri-hori-hai": 174,
    "stop-posting-about-among-us": 180,
    "dynamite": 181,
    "dna": 182,
    "its-my-life": 183,
    "scatman": 184,
    "toilet-2": 185,  # duplicate of 172
    "body": 186,
    "oh-no": 187,
    "safety-dance": 193,
    "runaway": 194,
    "mundian-to-bach-ke": 196,
    "money-money-money": 198,
    "gimme-more": 199,
    "california-gurls": 206,
    "fun-song-old": 207,  # 60fps; corrupt thumbnail
    "leave-the-door-open": 211,
    "look-at-me-now": 212,  # premium
    "stressed-out": 218,
    "fun-song": 220,  # 60fps; probably redone to fix the corrupt thumbnail
    "tusa": 245,
}


async def make_wombo(fp: FileIO, meme_name: str, session: ClientSession=None) -> str:
    print("Reserving upload location...")
    using_own_session = session is None
    if using_own_session:
        session = ClientSession()
    request_id, s3_fields = await step1(session, TOKEN)

    print("Uploading image...")
    im = Image.open(fp)
    rgb_im = im.convert("RGB")
    with TemporaryFile() as f_image:
        rgb_im.save(f_image)
        await step2(session, f_image, s3_fields)

    print("Beginning processing...")
    await step3(session, TOKEN, request_id, MEMES.get(meme_name, meme_name))

    video_url = await step4(session, TOKEN, request_id)

    if using_own_session:
        session.close()

    return video_url


async def step1(session: ClientSession, token: str) -> Tuple[str, S3Fields]:
    """ Reserve an S3 object to upload an image to """
    url = "https://api.wombo.ai/mobile-app/mashups/"
    headers = { "Authorization": f"Basic {token}" }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        data = await response.json()
        return (data["id"], data["upload_photo"]["fields"])


async def step2(session: ClientSession, f_image: FileIO, s3_fields: dict) -> None:
    """ Upload the image to the S3 location """
    with MultipartWriter() as mpwriter:
        for key in s3_fields:
            mpwriter.append(s3_fields[key], name=key)
        mpwriter.append(f_image, name="image.jpg")

        url = "https://wombo-user-content.s3.amazonaws.com/"
        async with session.post(url, data=mpwriter) as response:
            response.raise_for_status()


async def step3(session: ClientSession, token: str, request_id: str, meme_id: int) -> None:
    """ Request to begin processing on the uploaded image """
    url = f"https://api.wombo.ai/mobile-app/mashups/{request_id}"
    headers = { "Authorization": f"Basic {token}" }
    json = { "meme_id": str(meme_id), "premium": False }
    async with session.put(url, headers=headers, json=json) as response:
        response.raise_for_status()


async def step4(session: ClientSession, token: str, request_id: str) -> str:
    """ Poll for completion status """
    url = f"https://api.wombo.ai/mobile-app/mashups/{request_id}"
    headers = { "Authorization": f"Basic {token}" }
    while True:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            if data["state"] == "completed":
                return data["video_url"]
            elif data["state"] == "failed":
                raise Exception(f"Wombo generation failed: {data}")
            else:
                print(data["state"].capitalize() + "...")
                await asyncio.sleep(2)
