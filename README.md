A project that allows you to plan a flight between two airports and obtain flight parameters for the selected aircraft.

![version](https://img.shields.io/badge/version-3.0.1-blue)
![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![coverage](https://img.shields.io/badge/coverage-98%25-green)

## Usage
```ts
                                             ▏         Aircraft: b738 
                                             ▏         ULLI lat:59.800301, lon:30.262501
                                             ▏         UUEE lat:55.972599, lon:37.4146 
   from src.models.flight import Flight      ▏         Distance: 599 km
                                             ▏
   flight = Flight(                          ▏         Flight Passengers [max]: 184 
       dep_icao="ulli",                      ▏         Block Fuel: 6992 kg 
       arr_icao="uuee",                      ▏         Payload: 19136 kg
       aircraft_icao="b738"                  ▏         Cargo: 4784 kg
   )                                         ▏  
                                             ▏         ZFW est:60818, max:62732 
                                             ▏         TOW est:67810, max:79016
                                             ▏         LW est:65602, max:66361
```
## Tree
```php
.
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
```python
pytest -vv
```
```python
coverage run -m pytest
```
```python
coverage report
```