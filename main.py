from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from controllers.auth import AuthRouter
from controllers.user import UserRouter
from controllers.post import PostRouter
from controllers.follower import FollowerRouter
from controllers.search import SearchRouter
from controllers.comments import CommentsRouter

from models import user, post, view, follow, comments

user.initialise()
post.initialise()
view.initialise()
follow.initialise()
comments.initialise()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='secret')
app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
app.include_router(UserRouter, prefix="/user", tags=["user"])
app.include_router(PostRouter, prefix="/post", tags=["post"])
app.include_router(FollowerRouter, prefix="/follower", tags=["follower"])
app.include_router(SearchRouter, prefix="/search", tags=["search"])
app.include_router(CommentsRouter, prefix="/comment", tags=["comments"])

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return HTTPException(404)


uvicorn.run(app, host="0.0.0.0", port=8000)
