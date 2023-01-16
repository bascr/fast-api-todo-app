from fastapi import FastAPI
from database import engine
from routers import auth, todos, users, address
from company import companyapi
import models
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapi.router)
app.include_router(users.router)
app.include_router(address.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


