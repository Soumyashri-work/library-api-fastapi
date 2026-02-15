from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Author, Book, Category
from schemas import AuthorCreate, AuthorOut, BookCreate, BookOut, CategoryCreate, CategoryOut

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/authors", response_model=AuthorOut)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    obj = Author(**author.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.post("/categories", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    obj = Category(**category.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    obj = Book(**book.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/books", response_model=list[BookOut])
def list_books(
    author_id: int | None = None,
    category_id: int | None = None,
    year: int | None = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    q = db.query(Book)
    if author_id:
        q = q.filter(Book.author_id == author_id)
    if category_id:
        q = q.filter(Book.category_id == category_id)
    if year:
        q = q.filter(Book.publication_year == year)
    return q.limit(limit).all()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

@app.get("/stats/book-count")
def book_count(db: Session = Depends(get_db)):
    return {"total_books": db.query(Book).count()}

@app.get("/stats/average-year")
def average_year(db: Session = Depends(get_db)):
    years = [b.publication_year for b in db.query(Book).all() if b.publication_year]
    if not years:
        return {"message": "No books with publication year"}
    return {"average_year": sum(years) / len(years)}

@app.get("/stats/author-range/{author_id}")
def author_range(author_id: int, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author_id == author_id).all()
    if not books:
        return {"message": "No books for author"}
    books.sort(key=lambda b: b.publication_year or 0)
    return {
        "earliest": books[0].title,
        "latest": books[-1].title
    }

@app.get("/stats/author-has-books/{author_id}")
def author_has_books(author_id: int, db: Session = Depends(get_db)):
    exists = db.query(Book).filter(Book.author_id == author_id).first() is not None
    return {"has_books": exists}
