from fastapi import APIRouter, UploadFile, File, Form
from app.services.supabase import supabase
from app.core.config import settings
import pandas as pd
import io
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/csv")
async def upload_csv(
    file: UploadFile = File(...),
    dataset_name: str = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df = df.fillna("")

        # Step 1: Insert dataset
        dataset_id = str(uuid.uuid4())
        supabase.table("datasets").insert({
            "id": dataset_id,
            "name": dataset_name,
            "data": df.to_dict(orient="records"),
            "uploaded_by": None,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        # Step 2: Insert locations (if lat/lon present)
        inserted_count = 0

        for _, row in df.iterrows():
            try:
                lat = float(str(row.get("Latitude", "")).strip() or "nan")
                lon = float(str(row.get("Longitude", "")).strip() or "nan")
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue  # skip invalid coordinates

                name = row.get("Name", "Unnamed location")
                description = row.get("Description", "")
                geom = f"POINT({lon} {lat})"

                supabase.rpc("add_location_with_dataset", {
                    "name": name,
                    "description": description,
                    "geom_wkt": geom,
                    "uploaded_by": None,  # You can replace with actual user ID later
                    "dataset_id": dataset_id
                }).execute()

                inserted_count += 1
            except Exception:
                continue  # skip bad rows

        return {
            "message": f"✅ Uploaded {len(df)} records — {inserted_count} with location",
            "dataset_id": dataset_id,
            "dataset_name": dataset_name
        }

    except Exception as e:
        return {"error": str(e)}
