from fastapi import  HTTPException, Request
from app.core.security import decode_access_token, decode_refresh_token


async def get_current_username(request: Request) -> str:
    username = request.cookies.get("username") or "guest"
    access_token = request.cookies.get("access_token")
    if not username or not access_token:
        raise HTTPException(status_code=400, detail="Username or access token not found in cookies")
    decoded_token = decode_access_token(access_token)
    if not decoded_token or decoded_token.get("sub") != username:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token not found in cookies")

        decode_refresh_tk= decode_refresh_token(refresh_token)
        if not decode_refresh_tk or decode_refresh_tk.get("sub") != username:
            raise HTTPException(status_code=401, detail="Invalid access token")
        # raise HTTPException(status_code=401, detail="Invalid access token")
    return username
