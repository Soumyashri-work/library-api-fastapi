from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str]

class AuthorOut(AuthorCreate):
    id: int
    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str

class CategoryOut(CategoryCreate):
    id: int
    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int]
    author_id: int
    category_id: int

class BookOut(BookCreate):
    id: int
    class Config:
        orm_mode = True
