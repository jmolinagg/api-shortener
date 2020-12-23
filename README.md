# api-shortener

api-shortener is a Python API for making short URLs that redirect to another URL.

## Installation

* Use a Python Virtual Environment
* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

**Python**
```bash
pip install -r requirements.txt
```
**Python3**
```bash
pip3 install -r requirements.txt
```
## Usage

**Starting server process**
```bash
uvicorn main:app
```
By default it will run on localhost (http://127.0.0.1:8000)

**To test all the API requests navigate to:**
* http://127.0.0.1:8000/docs

## License
[MIT](https://github.com/HabibuGG/api-shortener/blob/main/LICENSE)
