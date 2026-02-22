from pydantic import BaseModel


class products_list(BaseModel): 
    id: int
    name: str
    desc: str
    price: float
    quantity: int


        