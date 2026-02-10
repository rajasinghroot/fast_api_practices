from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal,get_db
from app.models import User
from app.auth import hash_password, get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Users"]  # 👈 this replaces "default"
)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def list_users(
        request: Request,
        db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    print(current_user);
    if not current_user:
        return RedirectResponse("/login", status_code=302)

    users = db.query(User).all()
    return templates.TemplateResponse(
        "users_list.html",
        {"request": request, "users": users}
    )

@router.get("/users/create")
def create_user_page(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})

@router.post("/users/create")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    return RedirectResponse("/users", status_code=302)

@router.get("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse("/users", status_code=302)
