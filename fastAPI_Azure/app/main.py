from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# This end point is exposing environment variables and not safe for production use

# @app.get("/data")
# def data():
#     db_password = os.getenv("DB_PASSWORD")

#     api_base_url = os.getenv("API_BASE_URL")
#     log_level = os.getenv("LOG_LEVEL")
#     max_connections = os.getenv("MAX_CONNECTIONS")

#     return {
#         "DB_PASSWORD": db_password,
#         "API_BASE_URL": api_base_url,
#         "LOG_LEVEL": log_level,
#         "MAX_CONNECTIONS": max_connections,
#         "ENVIRONMENT": os.getenv("ENVIRONMENT")
#     }

# local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
