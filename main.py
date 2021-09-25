import uvicorn
from fastapi import FastAPI, Query
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

# Query Parameters and String Validations
@app.get("/items/")
async def read_item(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {'item_id': item_id, **item.dict()} # descomprime el diccionario
    if q:
        result.update({'q': q})
    return result

@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    
    return item_dict

# fake db
fake_items_db = [{"item_name": "uno"}, {"item_name": "dos"}, {"item_name": "tres"}]
# Multiple path and query parameters

@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(user_id: int, item_id:str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})    
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item
    


# Optional parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# Query Parameters


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# Path parameters containing paths

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# create a Enum Class
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# simple route

@app.get("/")
async def root():
    return {'items': 'items list'}

# dinamic route

# @app.get('/items/{items_id}')
# async def read_item(items_id: int):
#     return {'items_id': items_id}

# order matters

@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}

@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}
