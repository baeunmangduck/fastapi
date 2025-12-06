from fastapi import FastAPI, Form, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()


# response_class를 반드시 해야한다는 강제성은 없음 / default는 JSONResponse
@app.get("/res_json/{item_id}", response_class=JSONResponse)
async def res_json(item_id: int, q: str | None = None):
    return JSONResponse(
        content={"message": "hello", "item_id": item_id, "q": q},
        status_code=status.HTTP_200_OK,
    )


@app.get("/res_html/{item_id}", response_class=HTMLResponse)
async def res_html(item_id: int, item_name: str | None = None):
    html_string = f"""
    <html>
        <body>
            <h1>HTML RESPONSE</h1>
            <p>{item_id}</p>
            <p>{item_name}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_string, status_code=status.HTTP_200_OK)


# Get to Get
@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect {comment}")

    return RedirectResponse(
        url=f"/res_html/3?item_name={comment}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


# Post to Get -> 로그인할 때의 상황
# status_code = 302(GET 메서드로의 변환을 강제하고 있지 않음, 그러나 관행적으로 사용) VS 303 ( GET 메서드 변환을 강제)
@app.post("/create_redirect")
async def create_redirect(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id:{item_id}")
    print(f"item_name:{item_name}")

    return RedirectResponse(
        url=f"/res_html/{item_id}?item_name={item_name}",
        # status_code=status.HTTP_302_FOUND, # 관행
        status_code=status.HTTP_303_SEE_OTHER,  # 정석
    )


class Item(BaseModel):
    name: str
    desc: str
    price: float
    tax: float | None = None


class ItemRes(BaseModel):
    name: str
    desc: str
    price_with_tax: float


# response_model: 강제적인 validation
@app.post("/create_item/", response_model=ItemRes, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price

    item_res = ItemRes(name=item.name, desc=item.desc, price_with_tax=price_with_tax)

    return item_res
