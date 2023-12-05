from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd
import argparse
from sys import stderr


def parse_ing_kontoauszug(file: Path) -> pd.DataFrame:
    """
    Parses a given Kontoauszug PDF file and returns its contents as a pandas DataFrame.

    Parameters:
        file (Path): The path to the kontoauszug PDF file.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed data from the kontoauszug PDF file. The DataFrame has three columns: 'date' (datetime), 'description' (str), and 'amount' (float).
    """
    reader = PdfReader(file)
    results = {"date": [], "description": [], "amount": []}
    amount_regex = re.compile(r"(-?(\d{1,3}(\.\d{3})*|\d+),\d{2})$")
    date_regex = re.compile(
        r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)[0-9]{2}"
    )

    for page in reader.pages:
        content = page.extract_text(0)

        for line in content.split("\n"):
            amount = amount_regex.search(line)
            if amount is not None:
                date = date_regex.search(line)
                if date is not None:
                    date = date.group(0)
                    amount = amount.group(0)
                    description = line[len(date) : -len(amount)].strip()

                    amount = float(amount.replace(".", "").replace(",", "."))
                    results["date"].append(date)
                    results["amount"].append(amount)
                    results["description"].append(description)
    data = pd.DataFrame(results)
    data["date"] = pd.to_datetime(data["date"], format="%d.%m.%Y")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path",
        metavar="INPUT",
        type=str,
        help="Can be a file or a directory with the ING PDF files",
    )
    # -a, --account
    parser.add_argument(
        "-a",
        "--account",
        type=str,
        required=False,
        default="giro",
        help="Account type to parse if directory is specified e.g. Giro, Extra (Default: Giro)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default="ing_kontoauszug.csv",
        help="Output file (Default: ing_kontoauszug.csv)",
    )
    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file() and path.suffix == ".pdf":
        df = parse_ing_kontoauszug(Path(args.path))
    elif path.is_dir():
        df = []
        for file in path.glob("*.pdf"):
            if ("kontoauszug" in file.name.lower()) and (
                args.account.lower() in file.name.lower()
            ):
                df.append(parse_ing_kontoauszug(file))
        df = pd.concat(df)
    else:
        print(f"Invalid input: {path}", file=stderr)
        exit(1)

    df = df.sort_values("date", ascending=False)
    df.to_csv(args.output, index=False)
