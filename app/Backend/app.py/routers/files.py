from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from ..s3_client import upload_fileobj, generate_presigned_url
from ..db import files_coll
from ..config import get_settings
from datetime import datetime
import uuid

router = APIRouter(prefix="", tags=["files"])
settings = get_settings()

@router.post("/upload", status_code=201)
async def upload_file(user_id: str = None, file: UploadFile = File(...)):
    # Generate unique S3 key
    ext = file.filename.split(".")[-1]
    key = f"uploads/{uuid.uuid4().hex}.{ext}"

    # Upload to S3
    try:
        # file.file is a SpooledTemporaryFile; upload_fileobj expects file-like
        upload_fileobj(file.file, bucket=settings.AWS_S3_BUCKET, key=key, content_type=file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {e}")

    # Insert metadata to MongoDB
    meta = {
        "filename": file.filename,
        "content_type": file.content_type,
        "s3_key": key,
        "user_id": user_id,
        "uploaded_at": datetime.utcnow()
    }
    res = await files_coll.insert_one(meta)
    meta["id"] = str(res.inserted_id)
    return {"id": meta["id"], "filename": meta["filename"], "s3_key": meta["s3_key"]}

@router.get("/file/{file_id}")
async def get_file(file_id: str):
    doc = await files_coll.find_one({"_id": {"$oid": file_id}}) if False else None
    # Note: Mongo's ObjectId handling below - we will convert properly:
    from bson import ObjectId
    if not ObjectId.is_valid(file_id):
        raise HTTPException(status_code=400, detail="invalid file id")
    obj = await files_coll.find_one({"_id": ObjectId(file_id)})
    if not obj:
        raise HTTPException(status_code=404, detail="file not found")
    url = generate_presigned_url(settings.AWS_S3_BUCKET, obj["s3_key"])
    return {"url": url, "filename": obj.get("filename"), "content_type": obj.get("content_type")}
