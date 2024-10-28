from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Post(PostBase):
    user_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class Post_Vote(BaseModel):
    Post: Post
    votes: int

    class config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str   

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id: int
    like: bool