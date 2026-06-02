from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from . import crud, schemas, models, auth
from .database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/users/", response_model=schemas.UserOut)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await crud.create_user(db, user_in.username, user_in.password)
    return user

@router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    q = await db.execute(select(models.User).where(models.User.id == user_id))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/tasks/", response_model=schemas.TaskOut)
async def create_task(task_in: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task = await crud.create_task(db, current_user, task_in.title, task_in.description)
    return task

@router.get("/tasks/", response_model=list[schemas.TaskOut])
async def read_tasks(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.list_tasks(db, current_user.id)
