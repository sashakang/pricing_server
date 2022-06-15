from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"Hello": "World!"}