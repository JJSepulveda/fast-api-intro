"""
Hello world! de fastAPI
"""
# Fastapi
from fastapi import FastAPI

# Instanciar FastAPI
app = FastAPI()

# Path operation decoration
@app.get("/")
def home():
	return {"Hello": "World"}
