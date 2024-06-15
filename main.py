from typing import List, Optional
from uuid import UUID, uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#DB Connection
MongoURL = "mongodb+srv://metanatest:metanatest@cluster0.sgcmcsf.mongodb.net/metanatest?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MongoURL)
db = client["metanatest"]


class UserData(BaseModel):
    # id: Optional[str] = None
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
    # Note: I used a email validation to make sure already exisisting user dont get entered as new users !
    checkEmail = await usersdata.find_one({"email": userdata.email})
    if checkEmail is None:
        userdata_d = userdata.dict()
        await usersdata.insert_one(userdata_d)
    else:
        raise HTTPException(status_code=409, detail="A User already exist under that email")
    return userdata

@app.get("/usersdata/", response_model=List[UserData])
async def read_userdata():
    usersList = await usersdata.find().to_list(length=1000)
    #for user in usersList:
    #    user['_id'] = str(user['_id'])
    return usersList

@app.get("/userdata/{user_email}", response_model=UserData)
async def read_a_user(user_email: str):
    user = await usersdata.find_one({"email": user_email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/deleteuser/{user_email}")
async def delete_user(user_email: str):
    result = await usersdata.find_one({"email": user_email})
    if result is not None:
        await usersdata.delete_one({"email": user_email})
        return {"message": "User with email has been deleted"}
    else:
        return {"message": "User not found"}


@app.get("/")
async def root():
    try:
        # Attempt to list collections in the database
        db = client.get_database()
        collections = await db.list_collection_names()
        return {"message": "connection working", "collections": collections}
    except Exception as e:
        return {"message": "connection failed", "error": str(e)}
    # return {"message": "works"}
