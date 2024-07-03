#!/usr/bin/python3
import csv
import logging
import os
import sys
from pathlib import Path

import pystache


logger = logging.getLogger("mail-sender")
formatter = logging.Formatter(
    fmt="%(asctime)s\t%(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler = logging.FileHandler(Path("mail-sender.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def load_model(input_file: str | Path) -> str:
    try:
        with open(input_file, "r") as f:
            logger.info(f"Loading model from {input_file}")
            return f.read()
    except OSError as e:
        logger.error(e)
        logger.error("Could not open input file")


def create_files(template: Path,
                 data_file: Path,
                 id_col: str,
                 output_dir: Path,
                 delimiter: str = ";",
                 verbose: bool = True) -> None:
    # Load mustache model
    model = load_model(template)
    with open(data_file, "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        if id_col not in list(reader.fieldnames):
            logger.error(f"{id_col} is not a valid column of {data_file}")
            sys.exit(1)
        if not output_dir.exists():
            output_dir.mkdir()
        for k in reader:
            logger.debug(f"Processing {k[id_col]}")
            content = pystache.render(model, k)
            with open(Path(output_dir, k[id_col]), "w") as out_file:
                out_file.write(content)
            if verbose:
                print(content)
