from fastapi import FastAPI
from app.api import upload
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, export  # 👈 add export

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello from Railway"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(export.router)  # 👈 register /datasets and /locations