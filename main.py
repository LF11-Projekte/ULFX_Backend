from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from controllers.auth import AuthRouter
from controllers.user import UserRouter

from models import user, post, view, follow

user.initialise()
post.initialise()
view.initialise()
follow.initialise()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='secret')
app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
app.include_router(UserRouter, prefix="/user", tags=["user"])


@app.get("/")
async def root():
    return HTTPException(404)


uvicorn.run(app, host="0.0.0.0", port=8000)
