# main.py
from fastapi import FastAPI
from app.api.routes import router as email_router

app = FastAPI()


app.include_router(email_router, prefix="/api", tags=["Email Sender"])

@app.get('/')
async def index():
    return {"real": "Python"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )