from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    name: str
    price: float


@app.get("/item_admin/", response_class=HTMLResponse)
async def read_item_by_admin(request: Request, is_admin: str):
    item = Item(name="test", price=10.3)

    return templates.TemplateResponse(
        request=request,
        name="item_admin.html",
        context={"is_admin": is_admin, "item": item},
    )


@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    all_items = [Item(name=f"test_item_{i}", price=i) for i in range(1, 6)]
    return templates.TemplateResponse(
        request=request, name="item_for.html", context={"all_items": all_items}
    )


@app.get("/safe_item", response_class=HTMLResponse)
async def safe_items(request: Request):
    safe_string = '''
    <body>
        <h1>hello</h1>
        <p>bye</p>
    </body>
    '''

    return templates.TemplateResponse(
        request=request, name="safe.html", context={"safe_string": safe_string}
    )
