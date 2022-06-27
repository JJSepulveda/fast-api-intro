"""
Hello world! de fastAPI
"""
# Python
from typing import Optional # Para definir parametros opcionales
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# Fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status
from fastapi import HTTPException

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


class PersonBase(BaseModel):
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


class Person(PersonBase):
	password: str = Field(
		...,
		min_length=8,
	)


class PersonOut(PersonBase):
	pass


class LoginOut(BaseModel):
	username: str = Field(
		...,
		max_length=20,
		example="username1"
	)
	message: str = Field(default="Login Succesfully!")


# Path operation decoration
@app.get(
	path="/", 
	status_code=status.HTTP_200_OK
)
def home():
	return {"Hello": "World"}

# Request and response body

@app.post(
	path="/person/new", 
	response_model=PersonOut,
	status_code=status.HTTP_201_CREATED,
	tags=['persons']
)
def create_person(person: Person = Body(...)):
	return person

# Validations: Query parameters

@app.get(
	path="/person/detail",
	status_code=status.HTTP_200_OK,
	tags=['persons']
)
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

persons = [1, 2, 3, 4, 5]

@app.get(
	path="/person/detail/{person_id}",
	status_code=status.HTTP_200_OK,
	tags=['persons']
)
def show_person(
	person_id: int = Path(
		..., 
		gt=0,
		title="Person ID",
		description="The person ID",
		example=1
	)
):
	if person_id not in persons:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="This person doesn't exist"
		)

	return {person_id: "It exists!"}

# Validations: request body

@app.put(
	path="/person/{person_id}",
	status_code=status.HTTP_201_CREATED,
	tags=['persons']
)
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

# Forms

@app.post(
	path="/login",
	response_model=LoginOut,
	status_code=status.HTTP_200_OK
)
def login(
	username: str = Form(...),
	password: str = Form(...)
):
	return LoginOut(username=username)

# cookies and headers parameters

@app.post(
	path="/contact",
	status_code=status.HTTP_200_OK
)
def contact(
	first_name: str = Form(
		...,
		max_length=20,
		min_length=1
	),
	last_name: str = Form(
		...,
		max_length=20,
		min_length=1
	),
	email: EmailStr = Form(...),
	message: str = Form(
		...,
		min_length=20
	),
	user_agent: Optional[str] = Header(default=None),
	ads: Optional[str] = Cookie(default=None),
):
	return user_agent

# Files

@app.post(
	path="/post-image",
)
def post_image(
	image: UploadFile = File(...)
):
	return {
		"Filename": image.filename,
		"Format": image.content_type,
		"Size(kb)": round(len(image.file.read())/1024, ndigits=2)
	}