
from fastapi import APIRouter
from pydantic import BaseModel
from app.rags.rag import rag_query

router = APIRouter()

class QueryRequest(BaseModel):
    q: str

@router.post('/')
async def query(req: QueryRequest):
    hits = rag_query(req.q, top_k=3)
    return {'query': req.q, 'results': hits}
