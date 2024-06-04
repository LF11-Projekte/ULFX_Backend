from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from controllers.auth import AuthRouter
from controllers.user import UserRouter
from controllers.post import PostRouter
from controllers.follower import FollowerRouter
from controllers.search import SearchRouter

from models import user, post, view, follow

user.initialise()
post.initialise()
view.initialise()
follow.initialise()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='secret')
app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
app.include_router(UserRouter, prefix="/user", tags=["user"])
app.include_router(PostRouter, prefix="/post", tags=["post"])
app.include_router(FollowerRouter, prefix="/follower", tags=["follower"])
app.include_router(SearchRouter, prefix="/search", tags=["search"])


@app.get("/")
async def root():
    return HTTPException(404)


uvicorn.run(app, host="0.0.0.0", port=8000)
