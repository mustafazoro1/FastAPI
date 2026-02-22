from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import products_list as ProductModel
from database import SessionLocal, engine, Base
import database_models

app = FastAPI()

# Create all tables before anything else
Base.metadata.create_all(bind=engine)

@app.get("/")
def meet():
    return "i am meet & greet"


products = [
    ProductModel(id=1, name="Iphone", desc="REFURBISHED Iphone For Cheap", price=99.9, quantity=2),
    ProductModel(id=2, name="leptop", desc="Leptop For Cheap", price=999.9, quantity=1),
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def innit_db():
    try:
        db = SessionLocal()
        count = db.query(database_models.products_list).count()

        if count == 0:  
            for product in products:
                db.add(database_models.products_list(**product.model_dump()))
            db.commit()
        db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

innit_db()


@app.get("/products")
def All_Products(db: Session = Depends(get_db)):
    # db.query()

    db_products = db.query(database_models.products_list).all()

    return db_products


@app.get("/product/{id}")
def product_By_Id(id: int ,db: Session = Depends(get_db)):
    db_product = db.query(database_models.products_list).filter(database_models.products_list.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/product")
def Add_Product(product_item: ProductModel):
    products.append(product_item)
    return products
  
@app.put("/product")
def update_product(id: int, product_up: ProductModel):
    for p_u in range(len(products)):
        if products[p_u].id == id:
            products[p_u] = product_up
            return "succsesfull"
    
    return "no"

@app.delete("/product")
def delete_product(id: int):
    for p_d in range(len(products)):
        if products[p_d].id == id:
            del products[p_d]
            return {"Message": "succsesfull"}
        
    raise HTTPException(status_code=404 , detail= "product not found")