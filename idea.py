"""Experiments with DuckDB as Backend

1. Use pysearch() UDF for SQL queries.

2. Store source code in compressed Parquet files.
"""

import duckdb
import pathlib
import pandas as pd
import tree_sitter_languages as tsl
import json

from duckdb.typing import BLOB, VARCHAR

con = duckdb.connect('test.duckdb')
cpython = pathlib.Path('/Users/grantjenks/repos/cpython')
records = [{'path': str(path), 'content': path.read_bytes()} for path in cpython.glob('**/*.py')]
df = pd.DataFrame.from_records(records)
print(con.sql('DROP TABLE IF EXISTS source'))
print(con.sql('CREATE TABLE source AS SELECT * FROM df'))


def pysearch(pattern, content):
    print('parsing', content[:40])
    parser = tsl.get_parser('python')
    language = tsl.get_language('python')
    tree = parser.parse(content)
    root = tree.root_node
    query = language.query(pattern)
    captures = query.captures(root)
    points = sorted(set((node.start_byte, node.end_byte) for node, _ in captures))
    return json.dumps([{'start': start, 'end': end} for start, end in points])


print(pysearch('(expression_statement (string)) @stmt_str', b'# Hello\n"hello"\n'))

print(
    duckdb.sql(
        """
        SELECT
            STRUCT_EXTRACT(
                UNNEST(
                    FROM_JSON(
                        JSON(
                            '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]'
                        ),
                        '[{"a": "BIGINT", "b": "BIGINT"}]'
                    )
                ),
                'a'
            ) AS a
        """
    )
)

con.create_function('pysearch', pysearch, [VARCHAR, BLOB], VARCHAR)

df = con.sql(
    """
        SELECT
            path
            , pysearch('(expression_statement (string)) @stmt_str', content) AS result
        FROM (
            -- Use a subquery to execute pysearch() on only 1 row.
            -- If the LIMIT clause is moved to the outer query then
            -- pysearch() will execute on every row.
            SELECT path, content
            FROM source
            LIMIT 1
        )
    """
).df()
