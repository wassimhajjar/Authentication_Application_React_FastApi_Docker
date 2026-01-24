from .base import BaseRepository
from app.db.models.message import Message
from app.db.schemas.message import MessageInCreate
from typing import List
from app.core.security.authHandler import AuthHandler
from dotenv import load_dotenv
import os
from typing import Annotated,Union
from fastapi import Header,HTTPException 
from fastapi.security import OAuth2PasswordBearer 
import datetime

load_dotenv()

class MessageRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        
    
    def create_message(self,message_data:MessageInCreate,token):
        payload=AuthHandler.decode_jwt(token=token)
        print("payload",payload)
        user_id=payload["user_id"]
        newMessage=Message(**message_data.model_dump(exclude_none=True))
        newMessage.timestamps=datetime.datetime.now()
        newMessage.user_id=user_id
        self.session.add(instance=newMessage)
        self.session.commit()
        self.session.refresh(instance=newMessage)
        
        return newMessage
    
    def get_messages_by_userid(self,user_id,token)->List[Message]:
        payload=AuthHandler.decode_jwt(token=token)
        id=payload["user_id"]
        if user_id==id:
            messages=self.session.query(Message).filter_by(user_id=user_id)
            return {"messages":messages}
        else:
            raise HTTPException(status_code=404,detail="Not found")
            
    
    def get_message_by_id(self,message_id:int)->Message:
        message=self.session.query(Message).filter_by(id=message_id).first()
        return message
    
    def get_messages_by_role(self,role:str)->Message:
        messages=self.session.query(Message).filter_by(role=role)
        return messages