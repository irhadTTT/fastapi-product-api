from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.inventory_report import InventoryReportResponse
from services.inventory_report_service import InventoryReportService

router = APIRouter(prefix="/reports", tags=["Inventory reports"])


@router.get("/", response_model=InventoryReportResponse)
async def get_reports(low_stock_threshold: int = 10, db: Session = Depends(get_db)):
    return await InventoryReportService.get_inventory_summary(db, low_stock_threshold)
