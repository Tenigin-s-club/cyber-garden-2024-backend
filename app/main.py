from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as auth_router
from app.routers.offices import router as office_router
from app.routers.build import router as build_router


app = FastAPI(root_path='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

for router in [auth_router, office_router, build_router]:
    app.include_router(router)
