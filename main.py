from typing import List, Optional
from uuid import UUID, uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#DB Connection
MongoURL = "mongodb+srv://metanatest:metanatest@cluster0.sgcmcsf.mongodb.net/metanatest?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MongoURL)
db = client["metanatest"]


class UserData(BaseModel):
    # _id: Optional[str] = None
    firstname: str
    lastname: str
    email: str
    country: str
    phonenumber: str
    languagesandframeworks: str
    experience: int
    annualcompensation: str
    linkedinurl: str

# usersdata = []
usersdata = db.get_collection("metanatest")

@app.post("/userdata/", response_model=UserData)
async def create_userdata(userdata: UserData):
    # userdata.id = uuid4()
    userdata_d = userdata.dict()
    await usersdata.insert_one(userdata_d)

    # usersdata.append(userdata)
    return userdata

@app.get("/usersdata/", response_model=List[UserData])
async def read_userdata():
    usersList = await usersdata.find().to_list(length=1000)
    #for user in usersList:
    #    user['_id'] = str(user['_id'])
    return usersList

@app.get("/")
async def root():
    try:
        # Attempt to list collections in the database
        db = client.get_database()
        collections = await db.list_collection_names()
        return {"message": "connection working", "collections": collections}
    except Exception as e:
        return {"message": "connection failed", "error": str(e)}
    # return {"message": "Hello Chiran it works"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}