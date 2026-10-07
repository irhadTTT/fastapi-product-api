from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from schemas.inventory_report import InventoryReportResponse
from services.inventory_report_service import InventoryReportService
from services.s3_service import upload_file

router = APIRouter(prefix="/reports", tags=["Inventory reports"])


@router.get("/", response_model=InventoryReportResponse)
async def get_reports(low_stock_threshold: int = 10, db: Session = Depends(get_db)):
    return await InventoryReportService.get_inventory_summary(db, low_stock_threshold)


@router.get("/export/csv")
async def export_inventory_report(
    db: Session = Depends(get_db),
):
    output = await InventoryReportService.export_inventory_report(db)

    filename = (
        f"inventory_report_"
        f"{datetime.now(timezone.utc).strftime('%d.%m.%Y_%H-%M-%S')}.csv"
    )

    upload_file(
        output.getvalue().encode("utf-8"),
        f"exports/{filename}",
        "text/csv",
    )

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; filename=inventory_report_"
                f"{datetime.now(timezone.utc).strftime('%d.%m.%Y_%H-%M-%S')}.csv"
            )
        },
    )


@router.get("/report/export")
async def export_inventory_report_excel(
    db: Session = Depends(get_db),
):
    output = await InventoryReportService.export_inventory_report_excel(db)

    filename = (
        f"inventory_report_"
        f"{datetime.now(timezone.utc).strftime('%d.%m.%Y_%H-%M-%S')}.xlsx"
    )

    upload_file(
        output.getvalue(),
        f"exports/{filename}",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={"Content-Disposition": (f"attachment; filename={filename}")},
    )
