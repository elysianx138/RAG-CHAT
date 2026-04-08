from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")

def upload_file():

    # save file

    # run ingestion

    return {"status": "success"}