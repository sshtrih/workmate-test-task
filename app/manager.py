from typing import List, Dict

from utils import load_csv, parse_args, pretty_table
from filtration import FilterEngine
from aggregation import AggregatorEngine


class CSVManager:
    def __init__(self) -> None:
        self.data: List[Dict[str, str]] = None
        self.file: str = None
        self.filter: str | None = None
        self.aggregation: str | None = None

    def start_job(self) -> None:
        args = parse_args()

        self.file, self.filter, self.aggregation = (
            args.file,
            args.where,
            args.aggregate,
        )

        self.data = load_csv(self.file)

        if self.filter:
            self.apply_filter()

        if self.aggregation:
            self.apply_apply_aggregation()

        print(pretty_table(self.data))

    def apply_filter(self):
        new_filter: FilterEngine = FilterEngine(self.data)
        self.data = new_filter.apply_filter(self.filter)

    def apply_apply_aggregation(self):
        new_aggregator: AggregatorEngine = AggregatorEngine(self.data)
        self.data = new_aggregator.apply_aggregation(self.aggregation)
