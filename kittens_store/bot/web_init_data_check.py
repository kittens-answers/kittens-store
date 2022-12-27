import hashlib
import hmac
from typing import Final
from urllib.parse import parse_qsl

from kittens_store.bot.config import settings

secret_key: Final = hmac.new(
    "WebAppData".encode(), settings.TG_TOKEN.encode(), hashlib.sha256
).digest()


def check(init_data: str):
    init_dict = dict(parse_qsl(init_data))
    hash_str = init_dict.pop("hash", "")
    data_check_string = "\n".join(
        [f"{k}={init_dict[k]}" for k in sorted(init_dict.keys())]
    )
    data_check = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    return (data_check == hash_str, init_dict)
