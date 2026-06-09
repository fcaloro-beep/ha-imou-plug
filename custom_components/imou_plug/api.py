import hashlib
import time
import uuid

import aiohttp
import logging
_LOGGER = logging.getLogger(__name__)



class ImouApi:

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

        self.access_token = None
        self.domain = None
        self.token_expire = 0

    def _build_sign(self):
        timestamp = int(time.time())
        nonce = str(uuid.uuid4())

        sign_str = (
            f"time:{timestamp},"
            f"nonce:{nonce},"
            f"appSecret:{self.app_secret}"
        )

        sign = hashlib.md5(
            sign_str.encode()
        ).hexdigest()

        return timestamp, nonce, sign

    async def authenticate(self):

        timestamp, nonce, sign = self._build_sign()

        payload = {
            "system": {
                "ver": "1.0",
                "appId": self.app_id,
                "sign": sign,
                "time": timestamp,
                "nonce": nonce,
            },
            "id": str(uuid.uuid4()),
            "params": {},
        }

        async with aiohttp.ClientSession() as session:

            async with session.post(
                "https://openapi.easy4ip.com/openapi/accessToken",
                json=payload,
            ) as response:

                data = await response.json(content_type=None)

        result = data["result"]["data"]

        self.access_token = result["accessToken"]
        self.domain = result["currentDomain"]

        self.token_expire = (
            time.time()
            + result["expireTime"]
            - 3600
        )

    async def ensure_token(self):

        if (
            self.access_token is None
            or time.time() > self.token_expire
        ):
            await self.authenticate()

    async def get_properties(
        self,
        product_id,
        device_id,
        properties,
    ):

        await self.ensure_token()

        timestamp, nonce, sign = self._build_sign()

        payload = {
            "system": {
                "ver": "1.0",
                "appId": self.app_id,
                "sign": sign,
                "time": timestamp,
                "nonce": nonce,
            },
            "id": str(uuid.uuid4()),
            "params": {
                "token": self.access_token,
                "productId": product_id,
                "deviceId": device_id,
                "properties": properties,
            },
        }

        async with aiohttp.ClientSession() as session:

            async with session.post(
                f"{self.domain}/openapi/getIotDeviceProperties",
                json=payload,
            ) as response:

                data = await response.json(content_type=None)

        return data["result"]["data"]

    async def set_properties(
        self,
        product_id,
        device_id,
        properties,
    ):

        await self.ensure_token()

        timestamp, nonce, sign = self._build_sign()

        payload = {
            "system": {
                "ver": "1.0",
                "appId": self.app_id,
                "sign": sign,
                "time": timestamp,
                "nonce": nonce,
            },
            "id": str(uuid.uuid4()),
            "params": {
                "token": self.access_token,
                "productId": product_id,
                "deviceId": device_id,
                "properties": properties,
            },
        }

        async with aiohttp.ClientSession() as session:

            async with session.post(
                f"{self.domain}/openapi/setIotDeviceProperties",
                json=payload,
            ) as response:

                return await response.json(content_type=None)
