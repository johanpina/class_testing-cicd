# schemas.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str = None
    price: int
    on_offer: bool = False

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True