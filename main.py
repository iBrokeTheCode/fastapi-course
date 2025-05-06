from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home() -> dict[str, str]:
    return {"greeting": "Hello world!"}


@app.get("/greet/{name}")
async def greet(name: str) -> dict:
    return {"message": f"Hello {name}"}
