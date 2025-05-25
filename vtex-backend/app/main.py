from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware  # <--- importar esto
from concurrent.futures import ThreadPoolExecutor
import asyncio
from app.db import init_db
from app.schema import schema  
from app.logic import sincronizar_ordenes
import strawberry
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

executor = ThreadPoolExecutor(max_workers=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "VTEX Distribution Analysis API"}

@app.post("/sync-orders")
async def sync_orders(request: Request):
    body = await request.json()  
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, sincronizar_ordenes, body)
    return {"message": "Sincronización completada"}
