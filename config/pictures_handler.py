from fastapi import HTTPException, status, File, UploadFile
from PIL import Image as PILImage
import shutil
import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024
COMPRESSION_QUALITY = 70


def compress_image(input_path: Path, output_path: Path, quality: int = COMPRESSION_QUALITY):
    with PILImage.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, format="JPEG", quality=quality, optimize=True)


def upload_picture(upload_dir: Path, file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Wrong file type. You can upload only png, jpg, jpeg")
    file.file.seek(0, 2)
    file_size = file.file.tell()
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File size bigger then {MAX_FILE_SIZE}")
    unique_filename = f"{uuid.uuid4()}.jpg"
    temp_path = upload_dir / f"temp_{unique_filename}"
    final_path = upload_dir / unique_filename
    file.file.seek(0)
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    compress_image(temp_path, final_path)
    temp_path.unlink()
    return final_path
