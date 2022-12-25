import json

from fastapi import Form

from kittens_store.bot.web_init_data_check import check


class InitData:
    def __init__(
        self, init_data: str | None = Form(default=None, alias="initData")
    ) -> None:
        if init_data is None:
            self._is_valid = None
            self._data: dict[str, str] = {}
            self._parsed = None
        else:
            self._is_valid, self._data = check(init_data=init_data)
            self._parsed = None

    @property
    def query_id(self):
        return self._data["query_id"]

    @property
    def user_id(self):
        user = self._data["user"]
        return int(json.loads(user)["id"])

    @property
    def is_valid(self):
        return self._is_valid
