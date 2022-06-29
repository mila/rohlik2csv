#!/usr/bin/env python3

import argparse
import logging
import pathlib

import pandas as pd
import tabula

ITEM = "Položka"
QTY = "Množství"
PRICE = "Cena vč. DPH"

IGNORED_ROWS = [
    "Doprava",
    "Haléřové vyrovnání",
    "Cena celkem",
    "Rekapitulace DPH:",
    "Kredity - kompenzace",
    "Sleva",
]


def _clean_price(s):
    return s.str.replace(" Kč", "").str.replace(",", ".").str.replace(" ", "")


def _clean_rows(df):
    df = df.loc[~df[ITEM].isna() & ~df[PRICE].isna()]
    for key in IGNORED_ROWS:
        df = df.loc[df[ITEM] != key]
    return df


def read_pdf(path):
    logging.info(f"Reading file: {path}")
    tables = tabula.read_pdf(path, multiple_tables=False, pages="all")
    assert len(tables) == 1
    df = _clean_rows(tables[0])
    name = str(path.name)
    product = df[ITEM]
    qty = df[QTY].astype(float)
    price = df[PRICE].pipe(_clean_price).astype(float)
    return pd.DataFrame({"file": name, "product": product, "qty": qty, "price": price})


def _iter_paths(paths):
    for path in paths:
        path = pathlib.Path(path)
        if path.is_dir():
            yield from path.glob("*.pdf")
        else:
            yield path


def read_pdfs(paths):
    frames = []
    for path in _iter_paths(paths):
        df = read_pdf(path)
        frames.append(df)
    return pd.concat(frames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+")
    args = parser.parse_args()

    logging.basicConfig(level="INFO", format="%(message)s")
    df = read_pdfs(args.path)
    print(df.to_csv(index=False))
