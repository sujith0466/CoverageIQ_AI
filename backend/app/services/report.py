import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.report import report as report_repo
from app.schemas.report import ReportCreate, ReportUploadResponse
from app.models.report import ReportStatus

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
MAX_XML_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_ZIP_SIZE = 100 * 1024 * 1024 # 100 MB

class ReportService:
    @staticmethod
    async def upload_coverage_report(db: AsyncSession, file: UploadFile) -> ReportUploadResponse:
        filename = file.filename.lower()
        is_xml = filename.endswith('.xml')
        is_zip = filename.endswith('.zip')
        
        if not is_xml and not is_zip:
            return ReportUploadResponse(
                success=False,
                message="Invalid file type. Only .xml or .zip files are allowed."
            )
            
        if is_xml and file.content_type not in ["text/xml", "application/xml"]:
            return ReportUploadResponse(
                success=False,
                message="Invalid content type. Expected XML."
            )
            
        if is_zip and file.content_type not in ["application/zip", "application/x-zip-compressed"]:
            return ReportUploadResponse(
                success=False,
                message="Invalid content type. Expected ZIP."
            )
        
        # Validate size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if is_xml and file_size > MAX_XML_SIZE:
            return ReportUploadResponse(
                success=False,
                message=f"XML file exceeds maximum allowed size of {MAX_XML_SIZE // (1024*1024)} MB."
            )
            
        if is_zip and file_size > MAX_ZIP_SIZE:
            return ReportUploadResponse(
                success=False,
                message=f"ZIP file exceeds maximum allowed size of {MAX_ZIP_SIZE // (1024*1024)} MB."
            )
        
        try:
            # Create DB record first to get the UUID
            obj_in = ReportCreate(
                filename=file.filename,
                status=ReportStatus.UPLOADED
            )
            db_report = await report_repo.create(db, obj_in=obj_in)
            
            # Ensure upload directory exists
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            
            # Save file as <uuid>.xml
            save_path = os.path.join(UPLOAD_DIR, f"{db_report.id}.xml")
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            return ReportUploadResponse(
                success=True,
                report_id=db_report.id,
                filename=db_report.filename,
                status=db_report.status.value
            )
            
        except Exception as e:
            return ReportUploadResponse(
                success=False,
                message=f"An error occurred during upload: {str(e)}"
            )
