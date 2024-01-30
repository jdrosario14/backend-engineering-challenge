"""test_unbabel_cli.py"""
import unittest
from ..unbabel_cli import main


class TestMainFunction(unittest.TestCase):
    """TestMainFunction class"""

    # def test_main_with_valid_inputs(self):
    #     input_file = "backend-engineering-challenge/events.json"
    #     window_size = 10

    #     input_json = json.dumps(input_data)
    #     input_file = StringIO(input_json)

    #     # Mocking the main function's output (you can adjust this based on your expected output)
    #     expected_output = "Your expected output here"

    #     with unittest.mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
    #         main(input_file, window_size=window_size)

    #         # Optionally, you can check the output printed by your main function
    #         actual_output = mock_stdout.getvalue().strip()
    #         self.assertEqual(actual_output, expected_output)

    def test_main_with_non_existent_file(self):
        """Test with an invalid input file (non-existent file)"""
        with self.assertRaises(FileNotFoundError):
            main(input_file="non_existent_file.json", window_size=10)

    def test_main_with_invalid_window_size(self):
        """Test with an invalid input window_size (<= 0)"""
        with self.assertRaises(ValueError):
            main(input_file="nonexistent_file.json", window_size=0)


if __name__ == "__main__":
    unittest.main()
