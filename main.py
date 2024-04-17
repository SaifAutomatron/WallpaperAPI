import os

import uvicorn
from fastapi import FastAPI, Request, Depends, Query
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from routers import auth, wallpapers, admin, users
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(wallpapers.router)
app.include_router(admin.router)
app.include_router(users.router)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(
    request: Request,
    db: Session = Depends(get_db),
    category: str = Query(None, description="Filter wallpapers by category, leave this empty for all wallpapers"),
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    size: int = Query(10, ge=1, description="Number of items per page")
):
    query = db.query(models.Wallpapers)
    if category and category.strip():
        query = query.filter(models.Wallpapers.category == category)
    total_count = query.count()
    wallpapers_data = query.offset((page - 1) * size).limit(size).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "wallpapers": wallpapers_data,
        "total_count": total_count,
        "page": page,
        "size": size,
        "total_pages": (total_count + size - 1) // size
    })


if __name__ == "__main__":
    print("Strating webserver..")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        proxy_headers=True
    )