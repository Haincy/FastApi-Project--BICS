from fastapi import APIRouter

router = APIRouter(prefix="/halls", tags=["Halls"])

@router.get("/")
def get_halls():
    return {"message": "List of halls"}
