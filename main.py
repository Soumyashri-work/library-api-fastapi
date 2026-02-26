from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Author, Book, Category
from schemas import AuthorCreate, AuthorOut, BookCreate, BookOut, CategoryCreate, CategoryOut

app = FastAPI()

# ── CORS: lets React (localhost:5173) talk to FastAPI (localhost:8000) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# ────────────────────────────────────────────────────────────────────────
# AUTHORS
# ────────────────────────────────────────────────────────────────────────

@app.get("/authors", response_model=list[AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/authors/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    obj = db.get(Author, author_id)
    if not obj:
        raise HTTPException(404, "Author not found")
    return obj


@app.post("/authors", response_model=AuthorOut)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    obj = Author(**author.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/authors/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    obj = db.get(Author, author_id)
    if not obj:
        raise HTTPException(404, "Author not found")
    for k, v in author.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    obj = db.get(Author, author_id)
    if not obj:
        raise HTTPException(404, "Author not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}


# ────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ────────────────────────────────────────────────────────────────────────

@app.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.post("/categories", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    obj = Category(**category.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ────────────────────────────────────────────────────────────────────────
# BOOKS
# IMPORTANT: /books/insights MUST come BEFORE /books/{book_id}
# otherwise FastAPI treats "insights" as a book_id and crashes
# ────────────────────────────────────────────────────────────────────────

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


@app.get("/books/insights")
def books_insights(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    if not books:
        return {"top_authors": [], "busy_years": {}}

    valid_books = [
        b for b in books
        if b.author is not None
        and b.publication_year is not None
        and 1900 <= b.publication_year <= 2100
    ]

    if not valid_books:
        return {"top_authors": [], "busy_years": {}}

    author_counts = {}
    for book in valid_books:
        author_counts[book.author.name] = author_counts.get(book.author.name, 0) + 1

    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_authors_result = [{"author": name, "book_count": count} for name, count in top_authors]

    year_map = {}
    for book in valid_books:
        year_map.setdefault(book.publication_year, []).append(book.title)

    busy_years = {
        year: titles
        for year, titles in sorted(year_map.items())
        if len(titles) >= 2
    }

    return {"top_authors": top_authors_result, "busy_years": busy_years}


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    obj = db.get(Book, book_id)
    if not obj:
        raise HTTPException(404, "Book not found")
    return obj


@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    obj = Book(**book.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    obj = db.get(Book, book_id)
    if not obj:
        raise HTTPException(404, "Book not found")
    for k, v in book.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    obj = db.get(Book, book_id)
    if not obj:
        raise HTTPException(404, "Book not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}


# ────────────────────────────────────────────────────────────────────────
# STATS
# ────────────────────────────────────────────────────────────────────────

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
    return {"earliest": books[0].title, "latest": books[-1].title}


@app.get("/stats/author-has-books/{author_id}")
def author_has_books(author_id: int, db: Session = Depends(get_db)):
    exists = db.query(Book).filter(Book.author_id == author_id).first() is not None
<<<<<<< HEAD
    return {"has_books": exists}
=======
    return {"has_books": exists}

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    user = validate_credentials(request.headers.get("Authorization"))
    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    request.state.user = user
    return await call_next(request)

@app.get("/books/insights")
def books_insights(db: Session = Depends(get_db)):
    # 1. Load all books
    books = db.query(Book).all()

    if not books:
        return {
            "top_authors": [],
            "busy_years": {}
        }

    # 2. Filter valid books
    valid_books = []
    for book in books:
        if (
            book.author is not None
            and book.publication_year is not None
            and 1900 <= book.publication_year <= 2100
        ):
            valid_books.append(book)

    if not valid_books:
        return {
            "top_authors": [],
            "busy_years": {}
        }

    # 3. Top authors (count per author)
    author_counts = {}
    for book in valid_books:
        author_name = book.author.name
        author_counts[author_name] = author_counts.get(author_name, 0) + 1

    # Sort authors by book count (descending) and take top 5
    top_authors = sorted(
        author_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_authors_result = [
        {"author": name, "book_count": count}
        for name, count in top_authors
    ]

    # 4. Busy years (years with >= 2 books)
    year_map = {}
    for book in valid_books:
        year = book.publication_year
        year_map.setdefault(year, []).append(book.title)

    busy_years = {
        year: titles
        for year, titles in sorted(year_map.items())
        if len(titles) >= 2
    }

    # 5. Return report
    return {
        "top_authors": top_authors_result,
        "busy_years": busy_years
    }
>>>>>>> 14cad7c55bc534a8706c160d25e440fefed26e5e
