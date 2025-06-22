import pytest

from app.aggregation import AggregatorEngine


class TestAggregatorEngine:

    @pytest.mark.parametrize(
        "expression",
        [
            "priceavg",
            "price=",
            "=avg",
            "amount=avg",
            "price=sum",
            "",
            "price=avg=max",
        ],
    )
    def test_aggregation_invalid_expression(self, expression):

        data = [{"price": "10"}, {"price": "20"}]
        engine = AggregatorEngine(data)

        with pytest.raises(SystemExit):
            engine.apply_aggregation(expression)

    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("price=avg", [{"avg": "18.33"}]),
            ("price=max", [{"max": "30.0"}]),
            ("price=min", [{"min": "10.0"}]),
        ],
    )
    def test_aggregation_correct_result(self, expression, expected):
        data = [{"price": "10"}, {"price": "15"}, {"price": "30"}]
        engine = AggregatorEngine(data)
        result = engine.apply_aggregation(expression)
        assert result == expected

    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("price=avg", [{"avg": "15.33"}]),
            ("price=max", [{"max": "25.0"}]),
            ("price=min", [{"min": "5.5"}]),
        ],
    )
    def test_aggregation_floats(self, expression, expected):
        data = [{"price": "5.5"}, {"price": "15.5"}, {"price": "25.0"}]
        engine = AggregatorEngine(data)
        result = engine.apply_aggregation(expression)
        assert result == expected

    def test_aggregation_single_value(self):
        data = [{"price": "42"}]
        engine = AggregatorEngine(data)
        result = engine.apply_aggregation("price=avg")
        assert result == [{"avg": "42.0"}]
