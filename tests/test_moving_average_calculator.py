"""Test moving_average_calculator.py"""
import unittest
from datetime import datetime
from moving_average_calculator import moving_average


class TestMovingAverageCalculator(unittest.TestCase):
    """
    Unit tests for the moving_average function in the moving_average_calculator module.

    These tests cover the functionality of calculating the moving average of delivery time
    from a list of events.

    """

    def test_moving_average_empty_events(self):
        """
        Test the moving_average function with an empty list of events.

        Ensures that the function returns an empty list when given an empty list of events.

        """
        result = moving_average([], 5)
        self.assertEqual(result, [])

    def test_moving_average_single_event(self):
        """
        Test the moving_average function with a single event.

        Ensures that the function returns the correct result when given a list with a single event.

        """
        events = [{"datetime": datetime(2022, 1, 1, 12, 0), "duration": 10}]
        result = moving_average(events, 5)
        expected_result = [
            {"date": "2022-01-01 12:00:00", "average_delivery_time": 10.0},
            {"date": "2022-01-01 12:01:00", "average_delivery_time": 10.0},
        ]
        self.assertEqual(result, expected_result)

    def test_moving_average_multiple_events(self):
        """
        Test the moving_average function with multiple events.

        Ensures that the function returns the correct result when given a list with multiple events.

        """
        events = [
            {"datetime": datetime(2022, 1, 1, 12, 0), "duration": 10},
            {"datetime": datetime(2022, 1, 1, 12, 4), "duration": 15},
            {"datetime": datetime(2022, 1, 1, 12, 7), "duration": 20},
        ]
        result = moving_average(events, 5)
        expected_result = [
            {"date": "2022-01-01 12:00:00", "average_delivery_time": 10},
            {"date": "2022-01-01 12:01:00", "average_delivery_time": 10},
            {"date": "2022-01-01 12:02:00", "average_delivery_time": 10},
            {"date": "2022-01-01 12:03:00", "average_delivery_time": 10},
            {"date": "2022-01-01 12:04:00", "average_delivery_time": 12.5},
            {"date": "2022-01-01 12:05:00", "average_delivery_time": 12.5},
            {"date": "2022-01-01 12:06:00", "average_delivery_time": 15},
            {"date": "2022-01-01 12:07:00", "average_delivery_time": 17.5},
            {"date": "2022-01-01 12:08:00", "average_delivery_time": 17.5},
        ]
        self.assertEqual(result, expected_result)

    def test_moving_average_events_in_different_days(self):
        """
        Test the moving_average function with events spanning different days.

        Ensures that the function returns the correct number of entries when events span
        different days.

        """
        events = [
            {"datetime": datetime(2022, 1, 1, 12, 0), "duration": 10},
            {"datetime": datetime(2022, 1, 1, 12, 25), "duration": 20},
            {"datetime": datetime(2022, 1, 2, 10, 0), "duration": 35},
        ]
        result = moving_average(events, 30)
        self.assertEqual(len(result), 1322)
        self.assertEqual(
            result[0], {"date": "2022-01-01 12:00:00", "average_delivery_time": 10}
        )
        self.assertEqual(
            result[25], {"date": "2022-01-01 12:25:00", "average_delivery_time": 15}
        )
        self.assertEqual(
            result[1321], {"date": "2022-01-02 10:01:00", "average_delivery_time": 35}
        )


if __name__ == "__main__":
    unittest.main()
