from __future__ import annotations
import csv
import math
from dataclasses import dataclass
from typing import *
import sys
import unittest
sys.setrecursionlimit(10_000)


EXPECTED_HEADER = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]


@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]


@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node]


def parse_float(text: str) -> Optional[float]:
    """Convert a CSV field into a float, or None if the field is empty."""
    if text == "":
        return None
    return float(text)


def parse_row(fields: list[str]) -> Row:
    """Convert one CSV row into a Row object."""
    return Row(
        fields[0],
        int(fields[1]),
        parse_float(fields[2]),
        parse_float(fields[3]),
        parse_float(fields[4]),
        parse_float(fields[5]),
        parse_float(fields[6]),
        parse_float(fields[7]),
    )


def build_list(rows: list[Row]) -> Optional[Node]:
    """Recursively build a linked list from a list of Row objects."""
    if rows == []:
        return None
    return Node(rows[0], build_list(rows[1:]))


def read_csv_lines(filename: str) -> Optional[Node]:
    """Read a CSV file, validate its header, and return a linked list of rows."""
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        if header != EXPECTED_HEADER:
            raise ValueError

        rows = []
        for fields in reader:
            rows.append(parse_row(fields))

        return build_list(rows)


def listlen(data: Optional[Node]) -> int:
    """Return the number of nodes in a linked list."""
    if data is None:
        return 0
    return 1 + listlen(data.next)


def row_matches(row: Row, field_name: str, comparison: str, value: Union[str, float, int]) -> bool:
    """Return True if a row satisfies the requested comparison."""
    field_value = getattr(row, field_name)

    if field_value is None:
        return False

    if field_name == "country":
        if comparison != "equal":
            raise ValueError
        return field_value == value

    if comparison == "equal":
        return field_value == value
    elif comparison == "less_than":
        return field_value < value
    elif comparison == "greater_than":
        return field_value > value
    else:
        raise ValueError


def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:
    """Recursively filter rows in a linked list."""
    if data is None:
        return None

    filtered_rest = filter_rows(data.next, field_name, comparison, value)

    if row_matches(data.value, field_name, comparison, value):
        return Node(data.value, filtered_rest)
    else:
        return filtered_rest
