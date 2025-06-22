import pytest
from app.filtration import FilterEngine


class TestFilterEngine:

    @pytest.mark.parametrize(
        "filter_str",
        [
            "pricegt10",
            "rating>10",
            "price>abc",
            "price>",
            ">10",
            "price>",
            ">",
            "price=10=20",
            "=",
            "",
        ],
    )
    def test_invalid_filter_causes_exit(self, filter_str):
        data = [{"price": "10"}]
        engine = FilterEngine(data)

        with pytest.raises(SystemExit):
            engine.apply_filter(filter_str)

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price>15", [{"price": "20"}]),
            ("price>10", [{"price": "15"}, {"price": "20"}]),
            ("price>5", [{"price": "10"}, {"price": "15"}, {"price": "20"}]),
        ],
    )
    def test_filter_greater_than(self, filter_str, expected):
        data = [{"price": "10"}, {"price": "15"}, {"price": "20"}]
        engine = FilterEngine(data)
        result = engine.apply_filter(filter_str)
        assert result == expected

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price<15", [{"price": "10"}]),
            ("price<20", [{"price": "10"}, {"price": "15"}]),
            ("price<5", []),
        ],
    )
    def test_filter_less_than(self, filter_str, expected):
        data = [{"price": "10"}, {"price": "15"}, {"price": "20"}]
        engine = FilterEngine(data)
        result = engine.apply_filter(filter_str)
        assert result == expected

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price=10", [{"price": "10"}]),
            ("price=15", [{"price": "15"}]),
            ("price=999", []),
        ],
    )
    def test_filter_equal(self, filter_str, expected):
        data = [{"price": "10"}, {"price": "15"}, {"price": "20"}]
        engine = FilterEngine(data)
        assert engine.apply_filter(filter_str) == expected

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price>10.5", [{"price": "15.0"}, {"price": "20.25"}]),
            ("price>15.0", [{"price": "20.25"}]),
            ("price>21.0", []),
        ],
    )
    def test_filter_greater_than_floats(self, filter_str, expected):
        data = [{"price": "10.0"}, {"price": "15.0"}, {"price": "20.25"}]
        engine = FilterEngine(data)
        result = engine.apply_filter(filter_str)
        assert result == expected

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price<15.0", [{"price": "10.0"}]),
            ("price<20.25", [{"price": "10.0"}, {"price": "15.0"}]),
            ("price<5.5", []),
        ],
    )
    def test_filter_less_than_floats(self, filter_str, expected):
        data = [{"price": "10.0"}, {"price": "15.0"}, {"price": "20.25"}]
        engine = FilterEngine(data)
        result = engine.apply_filter(filter_str)
        assert result == expected

    @pytest.mark.parametrize(
        "filter_str, expected",
        [
            ("price=10.0", [{"price": "10.0"}]),
            ("price=20.25", [{"price": "20.25"}]),
            ("price=100.1", []),
        ],
    )
    def test_filter_equal_floats(self, filter_str, expected):
        data = [{"price": "10.0"}, {"price": "15.0"}, {"price": "20.25"}]
        engine = FilterEngine(data)
        assert engine.apply_filter(filter_str) == expected
