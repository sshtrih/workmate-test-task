import pytest

import sys
import os
import tempfile

from app.utils import parse_args, load_csv


class TestParseArgs:
    def test_parse_args_file_only(self, monkeypatch):
        test_args = ["prog", "--file=data.csv"]
        monkeypatch.setattr(sys, "argv", test_args)

        args = parse_args()
        assert args.file == "data.csv"
        assert args.where is None
        assert args.aggregate is None

    def test_parse_args_file_and_where(self, monkeypatch):
        test_args = ["prog", "--file=data.csv", "--where=price>10"]
        monkeypatch.setattr(sys, "argv", test_args)

        args = parse_args()
        assert args.file == "data.csv"
        assert args.where == "price>10"
        assert args.aggregate is None

    def test_parse_args_all_fields(self, monkeypatch):
        test_args = [
            "prog",
            "--file=data.csv",
            "--where=price>10",
            "--aggregate=price=avg",
        ]
        monkeypatch.setattr(sys, "argv", test_args)

        args = parse_args()
        assert args.file == "data.csv"
        assert args.where == "price>10"
        assert args.aggregate == "price=avg"

    def test_parse_args_missing_file(self, monkeypatch):
        test_args = ["prog", "--where=price>10"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_unknown_argument(self, monkeypatch):
        test_args = ["prog", "--file=data.csv", "--unknown=value"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit):
            parse_args()


class TestLoadCsv:
    def test_load_csv_success(self):
        with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False) as tmp:
            tmp.write("price,name\n10,apple\n20,banana\n")
            tmp_path = tmp.name

        try:
            result = load_csv(tmp_path)
            assert result == [
                {"price": "10", "name": "apple"},
                {"price": "20", "name": "banana"},
            ]
        finally:
            os.remove(tmp_path)


    def test_load_csv_file_not_found(self, monkeypatch):
        monkeypatch.setattr(
            sys, "exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code))
        )

        with pytest.raises(SystemExit):
            load_csv("non_existent_file.csv")
