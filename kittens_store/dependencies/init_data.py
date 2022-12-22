import hashlib
import hmac
from typing import Final
from urllib.parse import parse_qsl

from fastapi import Form

from kittens_store.bot.config import settings

secret_key: Final = hmac.new(
    "WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256
).digest()


class InitData:
    def __init__(
        self, init_data: str | None = Form(default=None, alias="initData")
    ) -> None:
        if init_data is None:
            self._is_valid = None
            self._data: dict[str, str] = {}
        else:
            init_dict = dict(parse_qsl(init_data))
            hash_str = init_dict.pop("hash", "")
            data_check_string = "\n".join(
                [f"{k}={init_dict[k]}" for k in sorted(init_dict.keys())]
            )
            data_check = hmac.new(
                secret_key, data_check_string.encode(), hashlib.sha256
            ).hexdigest()
            self._is_valid = data_check == hash_str
            self._data = init_dict

    @property
    def data(self):
        return self._data.copy()

    @property
    def is_valid(self):
        return self._is_valid
