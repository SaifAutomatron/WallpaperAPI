import json
import shutil

from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Depends, HTTPException, Path, APIRouter, UploadFile, File, Form, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from models import Wallpapers
from database import SessionLocal
from routers.auth import get_current_user
import httpx

router = APIRouter(
    prefix='/Wallpapers',
    tags=['Wallpapers']
)

templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class WallpaperRequest(BaseModel):
    title: str
    description: str
    category: str


# Siranjeevi's API
async def shorten_url(original_url: str) -> str:
    api_url = "http://shortlink.us-east-1.elasticbeanstalk.com/api/shortLink"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json={"URL": original_url})
            response.raise_for_status()
            result = response.json()
            return result.get("shortenedURL")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")


async def upload_image_and_get_url(image: UploadFile) -> str:
    api_url = "https://imageapi-0b331ab4caa4.herokuapp.com/upload"  # Replace with the actual API URL
    try:

        file_content = await image.read()
        image.filename = image.filename.replace(" ", "")
        files = {"image": (image.filename, file_content, image.content_type)}
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, files=files)
            response.raise_for_status()
            result = response.json()
            url = None# result['image_url']
            if url is not None:
                return url
            else:
                raise HTTPException(status_code=500, detail="Image URL was not returned from the server.")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
    except HTTPException as e:
        print(f"Image URL was not returned from the server")
    finally:
        await image.close()

    return "Upload failed or no URL returned"


@router.get("/upload")
async def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/api/upload", status_code=status.HTTP_201_CREATED)
async def upload_wallpapers(db: db_dependency, title: str = Form(...), description: str = Form(...),
                            category: str = Form(...), image: UploadFile = File(...), ):
    user = "user"
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed!")

    # Calling Salmaan's API
    image_url = await upload_image_and_get_url(image)
    print(image_url)
    # Calling Siranjeevi's API
    image_url = await shorten_url(image_url)
    wallpaper_data = {
        "title": title,
        "description": description,
        "category": category,
        "url": image_url,
        "owner_id": 13
    }
    wallpaper_model = Wallpapers(**wallpaper_data)
    db.add(wallpaper_model)
    db.commit()
    db.refresh(wallpaper_model)
    return {"message": "Wallpaper uploaded successfully", "image_url": image_url}


@router.get("/category/{category}", status_code=status.HTTP_200_OK)
async def get_wallpapers_by_category(category: str, db: Session = Depends(db_dependency), page: int = Query(1, ge=1, description="Page number starting from 1"),size: int = Query(10, ge=1, description="Number of items per page")):
    offset = (page - 1) * size
    wallpapers_data = db.query(Wallpapers).filter(Wallpapers.category == category).offset(offset).limit(size).all()

    if wallpapers_data:
        return wallpapers_data
    raise HTTPException(status_code=404, detail="No Wallpapers found for this category!")


@router.get("/delete")
async def get_upload_page(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@router.delete("/api/delete/{Wallpapers_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Wallpapers(Wallpapers_id: int, user: user_dependency, db: db_dependency, name: str = None):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed!")

    query = db.query(Wallpapers).filter(Wallpapers.id == Wallpapers_id, Wallpapers.owner_id == user.get("id"))
    if name:
        query = query.filter(Wallpapers.name == name)
    Wallpapers_data = query.first()
    if Wallpapers_data is None:
        raise HTTPException(status_code=404, detail="Wallpapers not found!")
    query.delete()
    db.commit()


@router.get("/update")
async def get_upload_page(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@router.put("/api/update/{Wallpapers_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_Wallpapers(Wallpapers_id: int, Wallpapers_request: WallpaperRequest, user: user_dependency,
                            db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed!")
    Wallpapers_data = db.query(Wallpapers).filter(Wallpapers.id == Wallpapers_id,
                                                  Wallpapers.owner_id == user.get("id")).first()
    if not Wallpapers_data:
        raise HTTPException(status_code=404, detail="Wallpapers not found!")

    for var, value in vars(Wallpapers_request).items():
        setattr(Wallpapers, var, value) if value is not None else None

    db.commit()
