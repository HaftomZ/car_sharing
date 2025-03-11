# from fastapi import APIRouter , Depends , status
# from schemas.reportSchema import ReportBase , ReportDisplay
# from sqlalchemy.orm import Session
# from config.db_connect import get_db
# from controller import reports
# from typing import List , Optional
# from controller.authentication import get_current_user
# from schemas.userSchema import UserBase 
# from schemas.adminSchema import AdminBase
# from enum import Enum

# router = APIRouter(
# prefix='/reports',
# tags=['reports']
# )

# class ReportStatus(str, Enum):
#     resolved = "resolved"
#     rejected = "rejected"
#     pending = "pending"

# #create report
# @router.post('/', response_model=ReportDisplay , status_code=status.HTTP_201_CREATED)
# def create_report(request: ReportBase , db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
#     return reports.create_report(db, request)


# #get all reports for specific creator or reported user or all
# @router.get('/', response_model=List[ReportDisplay])
# def get_all_reports(creator_id: int = None, reported_id: int = None, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
#     return reports.get_all_reports(db, creator_id, reported_id, current_user)


# #filter reports by admin on status
# @router.get('/filter', response_model=List[ReportDisplay])
# def filter_reports(report_status: ReportStatus, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
#     return reports.fiter_reports(db, report_status,current_user)


# #get report
# @router.get('/{id}', response_model=ReportDisplay)
# def get_report(id: int, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
#     return reports.get_report(db, id)


# #handle report by admin
# @router.put('/{id}')
# def handle_report(id: int, report_status: ReportStatus, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
#     return reports.handle_report(db, id , report_status, current_user)
