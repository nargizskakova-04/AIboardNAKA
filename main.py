from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware, HTTPException
from posts.router import router
from database import database
# from typing import List


app = FastAPI()
app.include_router(router, prefix="/posts")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
