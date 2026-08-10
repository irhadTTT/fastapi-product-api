import pytest

from services.inventory_report_service import InventoryReportService


@pytest.mark.asyncio
async def test_get_inventory_summary_from_cache(monkeypatch, db_session):
    cached_data = {
        "total_products": 10,
        "total_stock_units": 100,
        "low_stock_products": 3,
        "out_of_stock_products": 1,
        "inventory_value": 5000,
    }

    async def mock_get_cache(key):
        return cached_data

    def mock_get_inventory_summary(db, low_stock_threshold):
        raise AssertionError("Repository should not be called on cache")

    monkeypatch.setattr(
        "services.inventory_report_service.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.inventory_report_service.inventory_report_repository.get_inventory_summary",
        mock_get_inventory_summary,
    )

    result = await InventoryReportService.get_inventory_summary(db_session, 10)

    assert result.total_products == 10
    assert result.total_stock_units == 100
    assert result.low_stock_products == 3
    assert result.out_of_stock_products == 1
    assert result.inventory_value == 5000


@pytest.mark.asyncio
async def test_get_inventory_summary_cache_miss(monkeypatch, db_session):
    cache_data = {}

    async def mock_get_cache(key):
        return None

    def mock_get_inventory_summary(db, low_stock_threshold):
        return {
            "total_products": 10,
            "total_stock_units": 100,
            "low_stock_products": 3,
            "out_of_stock_products": 1,
            "inventory_value": 5000,
        }

    async def mock_set_cache(key, value, expire):
        cache_data["key"] = key
        cache_data["value"] = value
        cache_data["expire"] = expire

    monkeypatch.setattr(
        "services.inventory_report_service.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.inventory_report_service.inventory_report_repository.get_inventory_summary",
        mock_get_inventory_summary,
    )

    monkeypatch.setattr(
        "services.inventory_report_service.set_cache",
        mock_set_cache,
    )

    result = await InventoryReportService.get_inventory_summary(db_session, 10)

    assert result.total_products == 10
    assert result.total_stock_units == 100
    assert result.low_stock_products == 3
    assert result.out_of_stock_products == 1
    assert result.inventory_value == 5000

    assert cache_data["key"] == "inventory_report:10"
    assert cache_data["expire"] == 300
