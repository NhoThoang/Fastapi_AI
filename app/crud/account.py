from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select, exists
from sqlalchemy import select, exists, update, values
from fastapi import HTTPException, status
from app.models.accounts import Account
from app.models.user_devices import UserDevice
from app.schemas.account import AccountCreate, AccountBase, Optional
from app.core.security import get_password_hash, verify_password
from datetime import datetime

async def check_username_exists(session: AsyncSession, username: str, only_active: bool = False) -> bool:
    stmt = select(exists().where(Account.username == username))
    if only_active:
        stmt = stmt.where(Account.active.is_(True))
    result = await session.execute(stmt)
    return result.scalar()

async def create_account(session: AsyncSession, account: AccountCreate)-> Account:
    if await check_username_exists(session, account.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    hashed_password = get_password_hash(account.password)
    account_data = account.dict()
    account_data['password'] = hashed_password

    new_account = Account(**account_data)
    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)
    return new_account

async def check_login(session: AsyncSession, account: AccountBase)-> Optional[Account]:
    result = await session.execute(select(Account).where(Account.username == account.username))
    user = result.scalar()
    if user and verify_password(account.password, user.password):
        return user
    return None

async def get_refresh_token(session: AsyncSession, username: str) -> Optional[str]:
    result = await session.execute(select(Account.refresh_token).where(Account.username == username))
    refresh_token = result.scalar()
    return refresh_token

async def update_last_login (session: AsyncSession, device_id: str) -> bool:
    last_login = datetime.now()
    stmt = update(UserDevice).where(UserDevice.device_id == device_id).values(last_login=last_login)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
async def check_device_id_trusted(session: AsyncSession, username: str, device_id: str) -> bool:
    stmt = select(exists().where(
        UserDevice.username == username,
        UserDevice.device_id == device_id,
        UserDevice.is_trusted.is_(True)
    ))
    result = await session.execute(stmt)
    return result.scalar()
async def check_device_id_and_username_exists(session: AsyncSession, device_id: str, username: str) -> bool:
    stmt = select(exists().where(UserDevice.device_id == device_id, UserDevice.username == username))
    result = await session.execute(stmt)
    return result.scalar()
async def insert_user_device(
    session: AsyncSession,
    username: str,
    device_id: str,
    user_agent: str,
    ip_address: str) -> bool:
    if await check_device_id_and_username_exists(session, device_id, username):
        return False
    new_device = UserDevice(
        username=username,
        device_id=device_id,
        user_agent=user_agent,
        ip_address=ip_address
    )
    session.add(new_device)
    await session.commit()
    return True
async def update_refresh_token(session: AsyncSession, username: str, refresh_token: str) -> bool:
    stmt = update(Account).where(Account.username == username).values(refresh_token=refresh_token)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def update_trusted_devices(
    session: AsyncSession,
    username: str,
    device_id: str,
    is_trusted: bool) -> bool:
    stmt = update(UserDevice).where(
        UserDevice.username == username,
        UserDevice.device_id == device_id
    ).values(is_trusted=is_trusted)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

# async def get_account_by_username(session: AsyncSession, username: str) -> Account:
#     result = await session.execute(select(Account).where(Account.username == username))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user
