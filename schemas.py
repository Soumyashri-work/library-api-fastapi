from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorOut(AuthorCreate):
    id: int
    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str

class CategoryOut(CategoryCreate):
    id: int
    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    author_id: int
    category_id: int

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: Optional[int] = None
    author_id: Optional[int] = None      # None-safe: handles books with missing author
    category_id: Optional[int] = None    # None-safe: handles books with missing category
    class Config:
        from_attributes = True