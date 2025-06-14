from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from fastapi import Request
from app.schemas.account import AccountLogin, JsonOut, Accountusername
from app.core.security import *
from app.crud.account import *
router = APIRouter()
from datetime import timedelta
from app.core.config import Config
SECRET_HTTPS = Config.SECIRE_HTTPS
EXPIRATION_MAX_AGE = Config.EXPIRATION_MAX_AGE
SAMESITE = Config.SAMESITE
# def get_client_ip(request: Request) -> str:
#     return request.headers.get('X-Real-IP') or request.headers.get('X-Forwarded-For', request.remote_addr) or '0.0.0.0'
def get_client_ip(request: Request) -> str:
    return (
        request.headers.get('X-Real-IP')
        or request.headers.get('X-Forwarded-For')
        or request.client.host  # ✅ chính xác ở đây
        or '0.0.0.0'
    )
def get_user_agent(request: Request) -> str:
    return request.headers.get("User-Agent", "")

def set_auth_cookies(response: Response,username: str, access_token: str, refresh_token: str, csrf_token: str):
    response.set_cookie(
        key="username",
        value=username,
        httponly=False,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
def set_short_auth_cookies(response: Response, username: str, device_id: str, short_access_token: str, csrf_token: str):
    response.set_cookie(
        key="username",
        value=username,
        httponly=False,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="device_id",
        value=device_id,
        httponly=False,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="access_token",
        value=short_access_token,
        httponly=True,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=SECRET_HTTPS,
        samesite=SAMESITE,
        max_age=EXPIRATION_MAX_AGE
    )
def clear_auth_cookies(response: Response):
    for cookie_name in ["access_token", "refresh_token", "csrf_token"]:
        response.delete_cookie(cookie_name)

@router.post("/login", response_model=JsonOut, status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    response: Response,
    account: AccountLogin,
    session: AsyncSession = Depends(get_db)):
    user = await check_login(session=session, account=account)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials user or password wrong")
    access_token = create_access_token(data={"sub": user.username})
    csrf_token = generate_csrf_token()
    refresh_token = await get_refresh_token(session=session, username=user.username)
    if not refresh_token:
        first_login = True
    else:
        first_login = False
    if  await check_device_id_trusted(session=session, username=user.username, device_id=account.device_id):
        if not await update_last_login(session=session, device_id=account.device_id):
            raise HTTPException(status_code=500, detail="Failed to update last login time")
        trusted_device = True
    else:
        trusted_device = False
        refresh_token = create_refresh_token(data={"sub": user.username})
        await insert_user_device(
            session=session,
            username=user.username,
            device_id=account.device_id,
            user_agent = get_user_agent(request=request),
            ip_address = get_client_ip(request=request),
        )
        if first_login:
            await update_refresh_token(session=session, username=user.username, refresh_token=refresh_token)
    if first_login or trusted_device:
        set_auth_cookies(
            response=response,
            username=user.username,
            access_token=access_token,
            refresh_token=refresh_token,
            csrf_token=csrf_token
        )
        return {"status": "success", "message": "Login successful - first login or trusted device"}
    else:
        short_access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=1)
        )
        set_short_auth_cookies(
            response=response,
            username=user.username,
            device_id=account.device_id,
            short_access_token=short_access_token,
            csrf_token=csrf_token
        )
    return {"status": "new device", "message": "Login successful - untrusted device, short access token issued"}

@router.post("/update_trusted_device", response_model=JsonOut, status_code=status.HTTP_200_OK)
async def update_trusted_device(
    request: Request,
    response: Response,
    account: Accountusername,
    session: AsyncSession = Depends(get_db)):
    """
    Update the trusted status of a device for the user get username from cookies post.
    """
    username = request.cookies.get("username")
    device_id = request.cookies.get("device_id")
    access_token = request.cookies.get("access_token")
    csrf_token = request.cookies.get("csrf_token")
    if not username or not device_id or not access_token:
        raise HTTPException(status_code=400, detail="Username or device ID not found in cookies")
    username_decode_access_token = decode_access_token(token=access_token)
    if not username_decode_access_token or username_decode_access_token.get("sub") != account.username:
        raise HTTPException(status_code=401, detail="Invalid access token")
    await update_trusted_devices(session=session, username=username, device_id=device_id, is_trusted=True)
    refresh_token= await get_refresh_token(session=session, username=username)
    access_token = create_access_token(data={"sub": username})
    set_auth_cookies(
        response=response,
        username=username,
        access_token=access_token,
        refresh_token=refresh_token,
        csrf_token=csrf_token
        )
    return {"status": "success", "message": "Cookies and trusted device updated successfully"}