from sqlalchemy.orm.session import Session
from schemas.reportSchema import ReportBase
from models.Reports import DbReport
from models.Users import DbUser
from fastapi import HTTPException , status
from typing import Optional
from schemas.userSchema import userDisplay 

#create report
def create_report(db: Session, request: ReportBase, current_user: userDisplay):
    creator = db.query(DbUser). filter(DbUser.id == request.creator_id).first()
    if not creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Creator user is not existed")
    
    if request.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    reported = db.query(DbUser). filter(DbUser.id == request.reported_id).first()
    if not reported:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Reported user is not existed")
    
    if request.creator_id == request.reported_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="User can not report himself")
    
    new_report=DbReport(
            creator_id = request.creator_id,
            reported_id = request.reported_id,
            reason = request.reason,
            details = request.details
        )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report


#get all reports for specific creator or reported user or all
def get_all_reports(db: Session, creator_id: int, reported_id: int, current_user: userDisplay):
    report_query = db.query(DbReport)
    if creator_id is not None:
        if creator_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        report_query = report_query.filter(DbReport.creator_id == creator_id)

    elif reported_id is not None:
        if reported_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        report_query = report_query.filter(DbReport.reported_id == reported_id)

    else:
        if not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    return report_query.all()


#get report
def get_report(db: Session, id: int, current_user: userDisplay):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    report = db.query(DbReport).filter(DbReport.id == id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return report


#handle report
def handle_report(db: Session, id: int , report_status: str, current_user: userDisplay):

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    report = db.query(DbReport).filter(DbReport.id == id)
    if not report.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    report.update({
        DbReport.status : report_status
    })
    db.commit()
    return "Report status is updated"


#filter reports
def fiter_reports(db: Session, report_status: str, current_user: userDisplay):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    reports = db.query(DbReport).filter(DbReport.status == report_status).all()
    return reports
