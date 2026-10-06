from botocore.exceptions import ClientError
from fastapi import APIRouter, File, HTTPException, UploadFile

from services.s3_service import upload_file

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload")
async def upload_to_s3(file: UploadFile = File(...)):
    try:
        content = await file.read()

        upload_file(
            file_content=content, key=file.filename, content_type=file.content_type
        )

        return {"message": "File uploaded successfully", "filename": file.filename}

    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
