from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserData(BaseModel):
    id: Optional[UUID] = None
    firstname: str
    lastname: str
    email: str
    country: str
    phonenumber: str
    languagesandframeworks: str
    experience: int
    annualcompensation: str
    linkedinurl: str

usersdata = []

@app.post("/userdata/", response_model=UserData)
def create_userdata(userdata: UserData):
    userdata.id = uuid4()
    usersdata.append(userdata)
    return userdata

@app.get("/userdata/", response_model=List[UserData])
def read_userdata():
    return usersdata

@app.get("/")
async def root():
    return {"message": "Hello Chiran it works"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}