# Demo Flask App

This repository contains a demo Flask application written in Python. The purpose of this project is to learn Flask and practice building APIs using Python.

## Features

- A basic Flask web server
- API endpoints for demonstration
- Basic testing setup

## Installation

### Prerequisites

Make sure you have Python installed (preferably Python 3.8 or higher). You can check your Python version by running:

```sh
python --version
```

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/demo-flask-app.git
   cd demo-flask-app
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv .venv
   ```
3. Install dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

To start the Flask application, run:

```sh
python flask --app main run
```

This will start the development server, and you can access it at `http://127.0.0.1:5000/`.

## Running Tests

This repository includes a `Makefile` to help with running tests easily. To run the tests, simply execute:

```sh
make test
```

Ensure you have all necessary test dependencies installed before running tests.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or additional features.

## License

This project is licensed under the MIT License.
