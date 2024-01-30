"""Moving Average Calculator"""
from datetime import timedelta
from typing import List


def moving_average(events: List[dict], window_size: int) -> List[dict]:
    """
    Calculate the moving average of delivery time from a list of events for a specified window size.

    Parameters:
    - events (List[dict]): A list of events, where each event is represented as a dictionary
      with keys 'datetime' and 'duration'.
    - window_size (int): The size of the window (in minutes) for calculating the moving average.

    Returns:
    - List[dict]: A list of dictionaries representing the moving average results. Each dictionary
      contains keys 'date' (the timestamp for the result) and 'average_delivery_time'.

    Algorithm:
    1. Iterate over each minute within the time range of the events.
    2. For each minute, calculate the total duration and the number of events within the specified
       window.
    3. Update the 'first_non_expired' index to skip already processed events.
    4. Create a result dictionary for each minute and append it to the 'results' list.

    Note:
    - The 'events' list should be sorted by the 'datetime' key before calling this function.
    - The 'datetime' values in the events should be in ascending order.

    Example:
    - moving_average(events, window_size)

    Raises:
    - IndexError: If the 'events' list is empty.
    """

    # Return empty array if events list is empty
    if len(events) == 0:
        return []

    # List to store result objects (final output)
    results = []

    # Get datetime of first event rounded down to the minute (processing start point)
    first_datetime = events[0]["datetime"].replace(second=0, microsecond=0)

    # Get datetime of last event rounded up to the minute (processing end point)
    last_datetime = events[-1]["datetime"].replace(second=0, microsecond=0) + timedelta(
        minutes=1
    )

    # Get number of minutes present in events timestamp range (number of lines in output)
    num_minutes = int((last_datetime - first_datetime).total_seconds() / 60) + 1

    # Variable to store the index from the first non expired event (prevents expired events
    # to be iterated all the time)
    first_non_expired = 0

    # Iterate over each minute within the time range of the events
    for minute in range(0, num_minutes):
        # Total number of events to be considered for the current minute being processed
        num_events = 0
        # Sum of all durations from applicable events for the current minute being processed
        total_duration = 0

        # Current minute being processed (max time from window)
        current_time = first_datetime + timedelta(minutes=minute)
        # Current minute minus the window size minutes (min time from window)
        last_minutes_window = current_time - timedelta(minutes=window_size)

        # Iterate each event starting from the first non expired event
        for event in events[first_non_expired:]:
            if event["datetime"] <= current_time:
                if event["datetime"] >= last_minutes_window:
                    # Adds current event duration time to the total_duration and increment
                    # num_events if the event datetime is inside the window that is being processed
                    total_duration += event["duration"]
                    num_events += 1
                else:
                    # Increments the first_non_expired variable if the current event is expired
                    first_non_expired += 1
            else:
                break

        # Result object after processing
        result = {
            "date": str(current_time),
            "average_delivery_time": total_duration / num_events
            if num_events > 0
            else 0,
        }
        results.append(result)

    return results
