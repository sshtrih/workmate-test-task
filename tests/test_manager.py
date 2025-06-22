import pytest

from app.manager import CSVManager
from unittest import mock


class TestCSVManager:

    def test_apply_filter_changes_data(self):
        manager = CSVManager()
        manager.data = [{"price": "10"}, {"price": "20"}]
        manager.filter = "price>15"

        manager.apply_filter()

        assert manager.data == [{"price": "20"}]

    def test_apply_aggregation_changes_data(self):
        manager = CSVManager()
        manager.data = [{"price": "10"}, {"price": "30"}]
        manager.aggregation = "price=avg"

        manager.apply_apply_aggregation()

        assert manager.data == [{"avg": "20.0"}]

    def test_filter_then_aggregate(self):
        manager = CSVManager()
        manager.data = [{"price": "10"}, {"price": "20"}, {"price": "30"}]
        manager.filter = "price<25"
        manager.aggregation = "price=max"

        manager.apply_filter()
        manager.apply_apply_aggregation()

        assert manager.data == [{"max": "20.0"}]

    def test_parse_args_sets_all_values(self, monkeypatch):
        mock_args = mock.Mock()
        mock_args.file = "products.csv"
        mock_args.where = "price>10"
        mock_args.aggregate = "price=avg"

        monkeypatch.setattr("app.manager.parse_args", lambda: mock_args)
        monkeypatch.setattr(
            "app.manager.load_csv", lambda _: [{"price": "10"}, {"price": "20"}]
        )
        monkeypatch.setattr("app.manager.pretty_table", lambda data: "stub")

        manager = CSVManager()
        manager.start_job()

        assert manager.file == "products.csv"
        assert manager.filter == "price>10"
        assert manager.aggregation == "price=avg"
        assert manager.data == [{"avg": "20.0"}]
