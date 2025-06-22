import argparse
import csv
import sys

from typing import List, Dict, Any
from tabulate import tabulate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSV Processor")

    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--where", help='Filter condition, e.g. "price>500"')
    parser.add_argument("--aggregate", help='Aggregate condition, e.g. "price=avg"')

    return parser.parse_args()


def load_csv(filepath: str) -> List[Dict[str, str]]:
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)


def pretty_table(data: List[Dict[str, Any]]) -> str:
    return tabulate(data, headers="keys", tablefmt="grid")
