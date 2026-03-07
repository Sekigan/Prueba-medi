from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import db
import models


app = FastAPI()


models.Base.metadata.create_all(bind=db.engine)

@app.post("/customers/")
def create_costumer(name:str, email:str, city:str, db: Session = Depends(db.get_db)):
    new_customer = models.Customer(name=name, email=email, city=city)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

