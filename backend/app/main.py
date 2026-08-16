from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import tasks, projects, users
import time

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Capstone TaskFlow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} - {process_time:.2f}ms")
    return response

app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Capstone TaskFlow API is running"}