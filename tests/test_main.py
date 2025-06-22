from unittest import mock
from app.main import main


def test_main_calls_start_job():
    with mock.patch("app.main.CSVManager") as MockManager:
        instance = MockManager.return_value
        main()
        instance.start_job.assert_called_once()
