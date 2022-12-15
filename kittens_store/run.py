import uvicorn

if __name__ == "__main__":
    uvicorn.run("kittens_store.app:app", reload=True)
