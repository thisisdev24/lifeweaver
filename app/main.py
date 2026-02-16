
from fastapi import FastAPI
from app.api import ingest, query, suggest

app = FastAPI(title="LifeWeaver (Starter API)")

app.include_router(ingest.router, prefix='/ingest', tags=['ingest'])
app.include_router(query.router, prefix='/query', tags=['query'])
app.include_router(suggest.router, prefix='/suggest', tags=['suggest'])

@app.get('/ping')
async def ping():
    return {'status': 'alive'}
