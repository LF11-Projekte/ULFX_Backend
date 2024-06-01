from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse


from config import USERMANAGER_URL, TOKEN_REDIRECT_URL, FRONTEND_URL

import requests

AuthRouter = APIRouter()


@AuthRouter.get("/login")
def get_auth_login(request: Request):
    if request.session.get("token"):
        token = request.session.get("token")
        res = requests.get(f"{USERMANAGER_URL}/auth/verify", headers={"Authorization": f"Bearer {token}"})
        if res.status_code != 200:
            request.session.clear()
            return RedirectResponse(url=TOKEN_REDIRECT_URL)
    else:
        return RedirectResponse(url=TOKEN_REDIRECT_URL)
    return RedirectResponse(url=FRONTEND_URL)


@AuthRouter.get("/logout")
def get_auth_login(request: Request):
    request.session.copy()
    return RedirectResponse(url=FRONTEND_URL)


@AuthRouter.get("/token")
def get_auth_token(request: Request, token: str = ""):
    if token:
        res = requests.get(f"{USERMANAGER_URL}/auth/verify", headers={"Authorization": f"Bearer {token}"})
        if res.status_code != 200:
            request.session.clear()
            return RedirectResponse(url=TOKEN_REDIRECT_URL)
        request.session["token"] = token

    return RedirectResponse(url=FRONTEND_URL)
