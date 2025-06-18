from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mysql.account import AccountCreate, JsonOut
from app.crud.mysql import account as crud_account
from app.db.mysql.session import get_db
from fastapi import status

router = APIRouter()

@router.post("/create_account/", response_model=JsonOut, status_code=status.HTTP_200_OK)
async def create_user(user: AccountCreate, session: AsyncSession = Depends(get_db)):
    await crud_account.create_account(session, user)
    return {
        "status": "success",
        "message": "Account created successfully"
    }
