from fastapi import FastAPI

from routers import label

app = FastAPI()
app.include_router(
    label.router,
    prefix="/label",
    tags=["label"],
)
