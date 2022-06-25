"""
Hello world! de fastAPI
"""
# Python
from typing import Optional # Para definir parametros opcionales
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path

# Instanciar FastAPI
app = FastAPI()

# Enums
class HairColor(Enum):
	""" 
	clase para enumerar todas las opciones 
	disponibles para el campo hair_color de
	el modelo Person.
	"""
	white = "white"
	brown = "brown"
	black = "black"
	blonde = "blonde"
	red = "red"


# Models
class Location(BaseModel):
	city: str = Field(
		..., 
		min_length=1,
		max_length=50
	)
	state: str = Field(
		..., 
		min_length=1,
		max_length=50
	)
	country: str = Field(
		..., 
		min_length=1,
		max_length=50
	)

	class Config:
		""" 
		Clase para definir la información por defecto para las
		pruebas en la documentación interactiva
		"""
		schema_extra = {
			"example": {
				"city": "Zapopan",
				"state": "Jalisco",
				"country": "Mexico",
			}
		}

class Person(BaseModel):
	first_name: str = Field(
		..., 
		min_length=1,
		max_length=50,
		example="Juan"
	)
	last_name: str = Field(
		..., 
		min_length=1,
		max_length=50,
		example="Lopez"
	)
	age: int= Field(
		..., 
		gt=0,
		le=115,
		example=25
	)
	hair_color: Optional[HairColor] = Field(
		default=None,
		example="black"
	)
	is_married: Optional[bool] = Field(
		default=None,
		example=False
	)
	password: str = Field(
		...,
		min_length=8,
	)

	# class Config:
	# 	""" 
	# 	Clase para definir la información por defecto para las
	# 	pruebas en la documentación interactiva
	# 	"""
	# 	schema_extra = {
	# 		"example": {
	# 			"first_name": "Juan",
	# 			"last_name": "Sepulveda",
	# 			"age": 20,
	# 			"hair_color": "brown",
	# 			"is_married": False
	# 		}
	# 	}

class PersonOut(BaseModel):
	first_name: str = Field(
		..., 
		min_length=1,
		max_length=50,
		example="Juan"
	)
	last_name: str = Field(
		..., 
		min_length=1,
		max_length=50,
		example="Lopez"
	)
	age: int= Field(
		..., 
		gt=0,
		le=115,
		example=25
	)
	hair_color: Optional[HairColor] = Field(
		default=None,
		example="black"
	)
	is_married: Optional[bool] = Field(
		default=None,
		example=False
	)


# Path operation decoration
@app.get("/")
def home():
	return {"Hello": "World"}

# Request and response body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
	return person

# Validations: Query parameters

@app.get("/person/detail")
def show_person(
	name: Optional[str] = Query(
		None, 
		min_length=1, 
		max_length=50,
		title="Person name",
		description="This is the person name. It's between 1 and 50 characteres",
		example="Jose"
	),
	age: int = Query(
		...,
		title="Person Age",
		description="This is the person age. It's required",
		example=25
	) # los query parameters no suelen ser obligatorios
):
	return {name: age}

# Validations: Path parameters

@app.get("/person/detail/{person_id}")
def show_person(
	person_id: int = Path(
		..., 
		gt=0,
		title="Person ID",
		description="The person ID",
		example=1
	)
):
	return {person_id: "It exists!"}

# Validations: request body

@app.put("/person/{person_id}")
def update_person(
	person_id: int = Path(
		...,
		title="Person ID",
		description="This is the person ID",
		gt=0,
		example=1
	),
	person: Person = Body(...),
	location: Location = Body(...)
):
	# Unimos los dos json en uno solo
	results = person.dict()
	results.update(location.dict())

	return results
