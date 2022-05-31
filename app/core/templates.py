import os

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

template_dir = os.path.join(
    "/".join(os.path.dirname(__file__).split("/")[:-1]), "public", "templates"
)
templates = Jinja2Templates(directory=template_dir)


static_dir = os.path.join(
    "/".join(os.path.dirname(__file__).split("/")[:-1]), "public", "static"
)
static_files = StaticFiles(directory=static_dir)
