from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from models import search
from models.post import Post

SearchRouter = APIRouter()


class User(BaseModel):
    user_id: int


class SearchRequest(BaseModel):
    user: list[User] | None = None
    post: list[Post] | None = None


@SearchRouter.get("/")
def get_search(request: Request, aduser: str = None, title: str = None, teaser: str = None) -> SearchRequest:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_list = []
    post_list = []
    result = search.search(aduser, title, teaser)

    if result.get("user"):
        for x in result.get("user"):
            user_list.append(User(
                user_id=x.get("rowid")
            ))

    if result.get("post"):
        for x in result.get("post"):
            print(x)
            post_list.append(Post(
                id=x.get("rowid"),
                creator=x.get("creator"),
                thumbnail=x.get("thumbnail"),
                teaser=x.get("teaser"),
                title=x.get("title"),
                content=x.get("content"),
                created_at=x.get("created_at"),
                updated_at=x.get("updated_at"),
            ))

    return SearchRequest(user=user_list, post=post_list)
