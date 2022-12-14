from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path.cwd().joinpath("kittens_store/templates"))
