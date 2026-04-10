from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload, chat, send, archive, drive

app = FastAPI(title="אור הפרשה Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(send.router, prefix="/api")
app.include_router(archive.router, prefix="/api")
app.include_router(drive.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "or-haparasha-studio"}
