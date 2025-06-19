from fastapi import APIRouter
from app.services.supabase import supabase
from fastapi import Query

router = APIRouter()

@router.get("/datasets")
def get_datasets():
    try:
        response = supabase.table("datasets").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

@router.get("/locations")
def get_locations(dataset_id: str = Query(default=None)):
    try:
        query = supabase.table("locations").select("*")
        if dataset_id:
            query = query.eq("dataset_id", dataset_id)
        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}