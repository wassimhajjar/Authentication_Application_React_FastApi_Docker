from pydantic import BaseModel

#what to expect to receive from the front-end
class MessageInCreate(BaseModel):
    role:str
    content:str

#from the backend to the db
class MessageOutput(BaseModel):
   id:int
   user_id:int
   role:str
   content:str
   timestamps:str