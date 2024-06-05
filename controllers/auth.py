from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import json
import base64

from config import USERMANAGER_URL, TOKEN_REDIRECT_URL, FRONTEND_URL

from models import user

import requests

AuthRouter = APIRouter()


class StatusModel(BaseModel):
    authorized: bool


@AuthRouter.get("/login", description="""
Redirect to this route. This route will redirect to usermanager automatically with redirect parameters.
""")
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


@AuthRouter.get("/verify")
def get_auth_login(request: Request) -> StatusModel:
    if request.session.get("token"):
        return StatusModel(authorized=True)
    else:
        return StatusModel(authorized=False)


@AuthRouter.get("/logout")
def get_auth_login(request: Request):
    request.session.copy()
    return RedirectResponse(url=FRONTEND_URL)


@AuthRouter.get("/token", description="""
Only used for usermanager! After verifying token it will be redirected to frontend with token parameter.
""")
def get_auth_token(request: Request, token: str = ""):
    if token:
        res = requests.get(f"{USERMANAGER_URL}/auth/verify", headers={"Authorization": f"Bearer {token}"})
        if res.status_code != 200:
            request.session.clear()
            return RedirectResponse(url=TOKEN_REDIRECT_URL)
        request.session["token"] = token

        payload = token.split(".")[1]
        payload_decoded = base64.b64decode(f"{payload}==").decode("utf-8")
        aduser = json.loads(payload_decoded).get("user")
        request.session["aduser"] = aduser

        user_id = user.get_id(aduser).get("rowid")
        if user_id == -1:
            user_id = user.create(aduser)

        request.session["user_id"] = user_id

        return RedirectResponse(url=f"{FRONTEND_URL}?token={request.session.get('token')}")

    return HTTPException(400)
