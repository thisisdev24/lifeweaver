
from fastapi import APIRouter
from app.planner.planner import get_suggestions

router = APIRouter()

@router.get('/next_actions')
async def next_actions():
    return {'suggestions': get_suggestions()}
