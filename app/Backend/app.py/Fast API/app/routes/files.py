from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import os, uuid
from pymongo import MongoClient
import boto3
from bson import ObjectId

router = APIRouter()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/testdb")
mongo = MongoClient(MONGO_URI)
db = mongo.get_default_database()
files_col = db.files

s3 = boto3.client("s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION")
)
BUCKET = os.environ.get("S3_BUCKET", "my-temp-bucket")

@router.post("/upload")
async def upload_file(user_id: str, file: UploadFile = File(...)):
    contents = await file.read()
    key = f"uploads/{user_id}/{uuid.uuid4().hex}_{file.filename}"
    s3.put_object(Bucket=BUCKET, Key=key, Body=contents, ContentType=file.content_type)
    doc = {
        "user_id": user_id,
        "filename": file.filename,
        "s3_key": key,
        "content_type": file.content_type,
        "size": len(contents),
        "created_at": datetime.utcnow()
    }
    res = files_col.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.get("/file/{id}")
def get_presigned(id: str):
    doc = files_col.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="file not found")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": doc["s3_key"]}, ExpiresIn=3600)
    return {"url": url}
