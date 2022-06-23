"""
Hello world! de fastAPI
"""
# Python
from typing import Optional # Para definir parametros opcionales

# Pydantic
from pydantic import BaseModel

# Fastapi
from fastapi import FastAPI
from fastapi import Body

# Instanciar FastAPI
app = FastAPI()

# Models
class Person(BaseModel):
	first_name: str
	last_name: str
	age: int
	hair_color: Optional[str] = None
	is_married: Optional[bool] = None
	

# Path operation decoration
@app.get("/")
def home():
	return {"Hello": "World"}

# Request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
	return person
