A project that allows you to plan a flight between two airports and obtain flight parameters for the selected aircraft.

![version](https://img.shields.io/badge/version-4.0.1-blue)
![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![coverage](https://img.shields.io/badge/coverage-96%25-green)
![version](https://img.shields.io/badge/python-3.12-blue)
## Basic Usage
```py
from src.models.flight import Flight

flight = Flight(
    dep_icao="ulli",
    arr_icao="uuee",
    aircraft_icao="b738"
)                                               
```
## Оutput
The project now includes methods for both displaying and saving flight parameters. For example, the [save_to_json](src/models/flight.py) method allows saving flight data in [JSON format](docs/exemple-route-b738-ULLI-to-UUEE.json).
```php
flight.print_flight_params()    # Outputs data to the console
flight.save_to_json()           # Saves data to json file
```

## Tree
```py
.
├── docs/                            # Directory for documentation and code examples.
├── src/                             # Main directory for the project's source code.
│   ├── aircraft_data/               # Directory for aircraft data.
│   │   ├── json_data/               # JSON files containing aircraft data.
│   │   └── manufacturers/           # Directory for manufacturer-related files.
│   └── models/                      # Directory for the classes.
└── tests/                           # Directory for test files.
│
├── .env.example                     # Example environment variables file.
├── .gitignore                       # Specifies files and directories to ignore in Git.
├── example_code.py                  # Example code demonstrating the project's functionality.
├── LICENSE                          # License file for the project.
├── Маkеfile                         # File for managing build automation.
├── poetry.lock                      # File listing the exact versions of dependencies.
├── pyproject.toml                   # Configuration file for Poetry and project metadata.
├── setup.cfg                        # Configuration file for flake8 and isort.
└── README.md                        # Documentation file explaining the project.
```

## Installation
Clone the repository:
```ts
git clone https://github.com/onesch/Flight-Data-Calculation-opensource.git
```
Install dependencies:
```python
poetry install
```
Run the example code:
```python
poetry run python example_code.py
```

## Tests
```py
pytest -vv
```
```python
coverage run -m pytest
```
```python
coverage report
```

## Note
The project was created for aviation enthusiasts, intended for flight simulators.

Make a `.env` file in which you need to specify your [personal API key](https://www.checkwxapi.com/) `CHECK_WX_API`.