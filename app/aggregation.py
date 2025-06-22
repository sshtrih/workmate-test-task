from abc import ABC, abstractmethod
from typing import List, Dict

import sys


class Aggregator(ABC):
    @abstractmethod
    def compute(self, values: List[float]) -> float:
        pass


class AvgAggregator(Aggregator):
    def compute(self, values: List[float]) -> float:
        return sum(values) / len(values)


class MaxAggregator(Aggregator):
    def compute(self, values: List[float]) -> float:
        return max(values)


class MinAggregator(Aggregator):
    def compute(self, values: List[float]) -> float:
        return min(values)


class AggregatorEngine:
    SUPPORTED_COLUMNS = ["price"]
    AGGREGATOR_REGISTRY: dict[str, type[Aggregator]] = {
        "avg": AvgAggregator,
        "min": MinAggregator,
        "max": MaxAggregator,
    }

    def __init__(self, data: List[Dict[str, str]]) -> None:
        self.__data: List[Dict[str, str]] = data
        self.__column: str = None
        self.__operator: Aggregator = None
        self.__op: str = None

    def apply_aggregation(self, aggregation: str) -> List[Dict[str, str]]:
        self.__column, self.__operator, self.__op = self.__parse_agg_expression(
            aggregation
        )

        values = [float(row[self.__column]) for row in self.__data]
        result = self.__operator.compute(values)

        return [{self.__op: str(round(result, 2))}]

    def __parse_agg_expression(self, aggregation: str) -> tuple[str, str]:
        try:
            if "=" not in aggregation:
                print(
                    "[ERROR] Invalid aggregation format. Example: price=avg",
                    file=sys.stderr,
                )
                sys.exit(1)

            column, op = aggregation.split("=")

            if not self.__check_supported_columns(column):
                print(
                    f"[ERROR] Unsupported column for aggregation: '{column}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            if not self.__check_supported_aggregators(op):
                print(
                    f"[ERROR] Unsupported aggregator for aggregation: '{op}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            return column.strip(), self.__get_aggregator(op.strip()), op.strip()

        except ValueError as e:
            print(
                f"[ERROR] Failed to parse aggregation expression: {e}", file=sys.stderr
            )
            sys.exit(1)
        except Exception as e:
            print(
                f"[ERROR] Unexpected error while parsing aggregation: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    def __check_supported_columns(self, column: str) -> bool:
        return column in self.SUPPORTED_COLUMNS

    def __check_supported_aggregators(self, op: str) -> bool:
        return op in self.AGGREGATOR_REGISTRY

    def __get_aggregator(self, op: str) -> Aggregator:
        return self.AGGREGATOR_REGISTRY[op]()
