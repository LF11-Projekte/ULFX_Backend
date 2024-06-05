from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from models import search

SearchRouter = APIRouter()


@SearchRouter.get("/")
def get_search(request: Request, aduser: str = None, title: str = None, teaser: str = None):
    #if not request.session.get("token"):
    #    return HTTPException(403)
    return search.search(aduser, title, teaser)
