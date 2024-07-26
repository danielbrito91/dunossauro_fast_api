from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from duno_fast_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState
    created_at: datetime = None
    updated_at: datetime = None


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


# Campos opcionais no TodoUpdate
class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
