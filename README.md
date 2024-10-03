## Usage
![image](/examples/example_code.png "")
![image](/examples/example_input.png "")

```python
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
├── Makefile                         # File for managing build automation.
├── poetry.lock                      # File listing the exact versions of dependencies.
├── pyproject.toml                   # Configuration file for Poetry and project metadata.
└── README.md                        # Documentation file explaining the project.
```

## Version
```python
3.0.0
```

## Installation
Clone the repository:
```python
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
poetry run coverage run -m pytest
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
