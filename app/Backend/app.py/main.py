from fastapi import FastAPI
from .routers import users, posts, files

app = FastAPI(title="Files + Mongo + S3 API")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(files.router)
