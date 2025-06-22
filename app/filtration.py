from typing import List, Dict

import sys


class FilterEngine:
    SUPPORTED_OPERATORS = [">", "<", "="]
    SUPPORTED_COLUMNS = ["price"]

    def __init__(self, data: List[Dict[str, str]]) -> None:
        self.__data: List[Dict[str, str]] = data
        self.__column: str = None
        self.__operator: str = None
        self.__value: float = None

    def apply_filter(self, filter: str) -> List[Dict[str, str]]:
        self.__column, self.__operator, self.__value = self.__parse_filter_condition(
            filter
        )

        return [row for row in self.__data if self.__compare(float(row[self.__column]))]

    def __compare(self, cell: float) -> bool:
        if self.__operator == ">":
            return cell > self.__value
        if self.__operator == "<":
            return cell < self.__value
        return cell == self.__value

    def __parse_filter_condition(self, filter: str) -> tuple[str, str, str]:
        for op in self.SUPPORTED_OPERATORS:
            if op in filter:
                try:
                    column, value = filter.split(op)
                    column = column.strip()
                    value = value.strip()

                    if not self.__check_supported_columns(column):
                        print(
                            f"[ERROR] Unsupported column for filtering: '{column}'",
                            file=sys.stderr,
                        )
                        sys.exit(1)

                    return (column, op, float(value))

                except ValueError:
                    print(
                        f"[ERROR] Invalid value for filtering: value is not a number",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                except Exception as e:
                    print(
                        f"[ERROR] Unexpected error while parsing filter: {e}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

        print(
            f"[ERROR] No supported operator found in filter condition: '{filter}'",
            file=sys.stderr,
        )
        sys.exit(1)

    def __check_supported_columns(self, column: str) -> bool:
        return column in self.SUPPORTED_COLUMNS
