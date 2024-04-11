from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# backend
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
@app.get("/")
def root():
    return({ "message": "Welcome to the URL Shortener" })

@app.get("/url")
def url():
    return({ "message": "This is the URL endpoint" })

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
    