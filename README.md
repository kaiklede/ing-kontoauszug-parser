# ING Kontoauszug Parser
This is a simple parser for German ING (formerly ING DIBA) bank account statements. This is especially useful in combination with this account statement [download script](https://github.com/ja-ka/violentmonkey/tree/master).

## Setup
1. Clone or download the repository `git clone https://github.com/kaiklede/ing-kontoauszug-parser.git && cd ing-kontoauszug-parser`
2. install the dependencies `pip install -r requirements.txt`

## Usage
For example, if you want to parse `kontoauszug.pdf`:
```
python ingparser.py kontoauszug.pdf
```

You can use ```python ingparser.py --help``` to see further options

```
usage: ingparser.py [-h] [-a ACCOUNT] [-o OUTPUT] INPUT

positional arguments:
  INPUT                 Can be a file or a directory with the ING PDF files

options:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        Account type to parse if directory is specified e.g. Giro, Extra (Default: Giro)
  -o OUTPUT, --output OUTPUT
                        Output file (Default: ing_kontoauszug.csv)
```