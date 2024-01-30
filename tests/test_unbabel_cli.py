"""Test unbabel_cli.py"""
import json
import unittest
from io import StringIO
from datetime import datetime
from unittest.mock import patch
from unbabel_cli import main, parse_args, validate_args, handle_input_file


class TestUnbabelCli(unittest.TestCase):
    """
    Unit tests for utility functions in the unbabel_cli module and the entire flow of the program.

    These tests cover the functionality of parsing command-line arguments, validating input
    arguments, handling input files and the main flow of the program.

    """

    def test_parse_args(self):
        """
        Test the parsing of command-line arguments.

        Ensures that the `parse_args` function correctly parses and returns the provided
        command-line arguments.

        """
        args = [
            "unbabel_cli",
            "--input_file",
            "input.json",
            "--window_size",
            "10",
        ]

        with patch("sys.argv", args):
            args = parse_args()
            self.assertEqual(args.input_file, "input.json")
            self.assertEqual(args.window_size, 10)

    def test_validate_args_valid(self):
        """
        Test validation of valid input arguments.

        Ensures that the `validate_args` function does not raise an exception when provided
        with valid input arguments.

        """
        # Assuming a valid file path and window size
        try:
            validate_args("tests/fixtures/single_event.json", 10)
        except (ValueError, FileNotFoundError):
            self.fail("validate_args raised exception unexpectedly.")

    def test_validate_args_invalid_window_size(self):
        """
        Test validation of window size.

        Ensures that the `validate_args` function raises a `ValueError` when the window size
        is less than or equal to 0.

        """
        with self.assertRaisesRegex(
            ValueError, "The window size must be an integer greater than 0."
        ):
            validate_args("tests/fixtures/single_event.json", 0)

    def test_validate_args_file_not_found(self):
        """
        Test validation when the input file is not found.

        Ensures that the `validate_args` function raises a `FileNotFoundError` when the input
        file is not found.

        """
        with self.assertRaisesRegex(
            FileNotFoundError, "The file 'nonexistent_file.json' does not exist."
        ):
            validate_args("nonexistent_file.json", 10)

    def test_handle_input_file_empty_json(self):
        """
        Test handling of an empty JSON file.

        Ensures that the `handle_input_file` function raises a `ValueError` when attempting to
        handle an empty JSON file.

        """
        with self.assertRaisesRegex(ValueError, "The JSON file is empty."):
            handle_input_file("tests/fixtures/empty_events.json")

    def test_handle_input_file_valid_json(self):
        """
        Test handling of a valid JSON file.

        Ensures that the `handle_input_file` function correctly reads and processes the data
        from a valid JSON file.

        """
        data = [{"timestamp": "2022-01-01 12:00:00.000", "duration": 5}]
        with unittest.mock.patch(
            "builtins.open", unittest.mock.mock_open(read_data=json.dumps(data))
        ):
            result = handle_input_file("valid.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["datetime"], datetime(2022, 1, 1, 12, 0))
        self.assertEqual(result[0]["duration"], 5)

    @patch(
        "sys.argv",
        [
            "unbabel_cli.py",
            "--input_file",
            "tests/fixtures/unbabel_events.json",
            "--window_size",
            "10",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_flow(self, mock_stdout):
        """
        Test the entire flow of the program.

        Ensures that the main function processes input data, calculates moving averages,
        writes the result to a JSON file, prints the expected message, and verifies the
        correctness of the generated JSON file.

        """
        main()
        expected_output = "The result can be found in outputs/unbabel_events_10.json\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

        # Verify the correctness of the generated JSON file
        with open("outputs/unbabel_events_10.json", "r", encoding="utf-8") as json_file:
            result_data = json.load(json_file)

        # Assuming you have an expected result for the JSON content
        expected_result = [
            {"date": "2018-12-26 18:11:00", "average_delivery_time": 0},
            {"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0},
            {"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0},
            {"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0},
            {"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0},
            {"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0},
            {"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0},
            {"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5},
        ]

        self.assertEqual(result_data, expected_result)


if __name__ == "__main__":
    unittest.main()
