"""
Hello world! de fastAPI
"""
# Python
from typing import Optional # Para definir parametros opcionales

# Pydantic
from pydantic import BaseModel

# Fastapi
from fastapi import FastAPI
from fastapi import Body, Query

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

# Validations: Query parameters

@app.get("/person/detail")
def show_person(
	name: Optional[str] = Query(None, min_length=1, max_length=50),
	age: int = Query(...) # los query parameters no suelen ser obligatorios
):
	return {name: age}
