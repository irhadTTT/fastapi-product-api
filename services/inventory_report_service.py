import csv
from io import BytesIO, StringIO

from openpyxl import Workbook
from sqlalchemy.orm import Session

from core.logging import logger
from repositories import inventory_report_repository
from schemas.inventory_report import InventoryReportResponse
from services.cache_service import get_cache, set_cache


class InventoryReportService:
    @staticmethod
    async def get_inventory_summary(db: Session, low_stock_threshold: int):
        cache_key = f"inventory_report:{low_stock_threshold}"

        cached = await get_cache(cache_key)

        if cached:
            logger.debug("Inventory report fetched from cache")

            return InventoryReportResponse.model_validate(cached)

        inventory_report = inventory_report_repository.get_inventory_summary(
            db, low_stock_threshold
        )

        logger.info("Inventory report fetched from database")

        response = InventoryReportResponse.model_validate(inventory_report)

        await set_cache(
            cache_key,
            response.model_dump(mode="json"),
            expire=300,
        )

        logger.debug("Inventory report cache updated")

        return response

    @staticmethod
    async def export_inventory_report(
        db: Session,
        low_stock_threshold: int = 10,
    ):
        report = await InventoryReportService.get_inventory_summary(
            db,
            low_stock_threshold,
        )

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Total Products",
                "Total Stock Units",
                "Low Stock Products",
                "Out Of Stock Products",
                "Inventory Value",
            ]
        )

        writer.writerow(
            [
                report.total_products,
                report.total_stock_units,
                report.low_stock_products,
                report.out_of_stock_products,
                report.inventory_value,
            ]
        )

        output.seek(0)

        return output

    @staticmethod
    async def export_inventory_report_excel(
        db: Session,
        low_stock_threshold: int = 10,
    ):
        report = await InventoryReportService.get_inventory_summary(
            db,
            low_stock_threshold,
        )

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Inventory Report"

        worksheet.append(
            [
                "Total Products",
                "Total Stock Units",
                "Low Stock Products",
                "Out Of Stock Products",
                "Inventory Value",
            ]
        )

        worksheet.append(
            [
                report.total_products,
                report.total_stock_units,
                report.low_stock_products,
                report.out_of_stock_products,
                report.inventory_value,
            ]
        )

        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        return output
