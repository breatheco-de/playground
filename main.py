import re

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import api

template = None
with open("./static/index.html", "r") as f:
    template = f.read()


app = FastAPI(
    title="4Geeks Playground",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=['*'],
)


for mod in api.__all__:
    if re.search("pycache", mod.__name__):
        continue
    name = re.sub(r"api\.", "", mod.__name__)
    subapp: FastAPI = getattr(mod, "app")
    # Montar talent-tracker en /tracker/api/v1, el resto igual
    if name == "talent-tracker":
        app.mount("/tracker/api/v1", subapp, name)
    else:
        app.mount(f"/{name}", subapp, name)

app.mount("/static", StaticFiles(directory="static"), name="static")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/", include_in_schema=False)
async def app_root(request: Request):
    routes = ""
    for mod in api.__all__:
        if re.search("pycache", mod.__name__):
            continue
        name = re.sub("api\.", "", mod.__name__)
        mod_app = getattr(mod, "app", dict())
        if name == "talent-tracker":
            url = "/tracker/api/v1/docs"
        else:
            url = f"/{name}/docs"
        routes += f"""<li><a href="{url}">{getattr(mod_app, "title", "")}</a></li>"""
    return HTMLResponse(
        content=re.sub(
            r"{{ content }}",
            f"{routes}",
            template
        )
    )



# Favicon global para toda la app (Swagger, etc.)
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/4geeks.ico")
