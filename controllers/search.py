from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from models import search
from models.post import Post

SearchRouter = APIRouter()


class SearchRequest(BaseModel):
    user: list | None = None
    post: list[Post] | None = None


@SearchRouter.get("/")
def get_search(request: Request, aduser: str = None, title: str = None, teaser: str = None) -> SearchRequest:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    x = search.search(aduser, title, teaser)

    return SearchRequest(user=x.get("user"), post=x.get("post"))
