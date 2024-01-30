# Backend Engineering Challenge

This is a project for the Unbabel Backend Engineering Challenge and the goal of this challenge is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

## Requirements
+ Python 3

## Run
To run the program use the following command: 

```
python3 unbabel_cli.py --input_file <file.json> --window_size <window size>
```

**Input**:
+ ```input_file```: The path to the input JSON file containing the translation events.
+ ```window_size```: The window size in minutes to be used on the moving average calculations.

There are already some examples of input files to be used as arguments. These files can be found in the following path: ```tests/fixtures```. For instance, to use the example provided in the challenge description you can run the following command:

```
python3 unbabel_cli.py --input_file tests/fixtures/unbabel_events.json --window_size 10
```

**Output**:

The program will create a JSON file with the final response and this file can be found in the ```outputs``` folder. The file name will be a concatenation between the name of the input file and the window_size value passed as arguments. So for the example above the program will generate a file called ```unbabel_events_10.json``` inside the ```outputs``` folder.

## Tests
There are two test files:
+ ```test_unbabel_cli.py``` - Unit tests for utility functions in the unbabel_cli module and the entire flow of the program.
+ ```test_moving_average_calculator.py``` - Unit tests for the moving_average function in the moving_average_calculator module. 

To run the tests use the following commands:
+ test_unbabel_cli: ```python3 -m unittest tests.test_unbabel_cli```
+ test_moving_average_calculator: ```python3 -m unittest tests.test_moving_average_calculator```

## Assumptions
+ The input file must be a JSON file with a format like so:
```json
[
	{
    "timestamp": "2018-12-26 18:11:08.509654",
    "translation_id": "5aa5b2f39f7254a75aa5",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "airliberty",
    "event_name": "translation_delivered",
    "nr_words": 30,
    "duration": 20
  },
  {
    "timestamp": "2018-12-26 18:15:19.903159",
    "translation_id": "5aa5b2f39f7254a75aa4",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "airliberty",
    "event_name": "translation_delivered",
    "nr_words": 30,
    "duration": 31
  },
  {
    "timestamp": "2018-12-26 18:23:19.903159",
    "translation_id": "5aa5b2f39f7254a75bb3",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "taxi-eats",
    "event_name": "translation_delivered",
    "nr_words": 100,
    "duration": 54
  }
]
```
+ The elements in the input are ordered by the timestamp key, from lower (oldest) to higher values
