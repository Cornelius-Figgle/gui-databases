# GUI Databases Project (PyQt6)

Project for my college course.

## Installation

1. Ensure [Poetry](https://python-poetry.org/) is installed (either via [pipx](https://pipx.pypa.io/stable/) or [uv](https://docs.astral.sh/uv/)):

```shell
poetry --version
```

2. Clone this repo (or download and extract the zip/tarball)

```shell
git clone https://github.com/Cornelius-Figgle/gui-databases
cd gui-databases
```

3. Install the required dependencies

```shell
poetry install
```

## Usage

```shell
poetry run python3 gui_databases/frontend.py
```

On first run, the program should create a default user (username: `admin`, password: `admin`) for you.

### Troubleshooting

If you receive a `ModuleNotFound` error when running (mainly occurs on Windows), then switch `python3` for `python`:

```shell
poetry run python gui_databases/frontend.py
```

## External Libraries Used

- [qtawesome](https://qtawesome.readthedocs.io/en/latest/index.html)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)

## Sources Used

- [PythonGUIs PyQt6 Basic Tutorial](https://www.pythonguis.com/pyqt6-tutorial/)
- [Python Type Hints Specification](https://docs.python.org/3/library/typing.html)
- My own previous projects:
  - [Login Feature Project](https://github.com/Cornelius-Figgle/login-project/)
  - [Noughts & Crosses Project (PyQt6)](https://github.com/Cornelius-Figgle/noughts-crosses-qt6/)

## License

My code in this project is licensed under the MIT License, as found in the `LICENSE` file. 

Please refer to the linked libraries/sources for other possibly-applicable licenses. 
