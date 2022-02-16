from dataclasses import dataclass
from typing import List, Optional

from sqlite3 import Connection


@dataclass
class Column:
    name: str
    type: str
    default: Optional[str] = None

    @property
    def create_string(self) -> str:
        if self.default:
            return f"{self.name} {self.type} {self.default}"
        return f"{self.name} {self.type}"


@dataclass
class Table:
    name: str
    columns: List[Column]

    @property
    def create_table_statement(self) -> str:
        column_string = ", ".join(map(lambda x: x.create_string, self.columns))
        return f"create table if not exists {self.name} ({column_string})"

    def ensure(self, connection: Connection):
        with connection as con:
            con.execute(self.create_table_statement)


def initialize(con: Connection):
    stats_table = Table(
        name="solution_stats",
        columns=[
            Column(name="date", type="date"),
            Column(name="puzzle_number", type="INT"),
            Column(name="word", type="TEXT"),
            Column(name="results", type="INT"),
            Column(name="pct_1", type="REAL"),
            Column(name="pct_2", type="REAL"),
            Column(name="pct_3", type="REAL"),
            Column(name="pct_4", type="REAL"),
            Column(name="pct_5", type="REAL"),
            Column(name="pct_6", type="REAL"),
            Column(name="pct_fail", type="REAL"),
            Column(name="modal_score", type="TEXT"),
        ],
    )
    stats_table.ensure(con)