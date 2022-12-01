from csv import DictReader

from alembic import op
import sqlalchemy as sa


def copy_from_csv(
    f, schema, table, dest_cols=None, source_cols=None, header=True, encoding=None, delimiter=None
):
    """
    Insert CSV file into specified table.
    If source columns are specified, CSV file in copied in a temporary table,
    then data restricted to specified source columns are copied in final table.
    """

    dest_cols = " (" + ", ".join(dest_cols) + ")" if isinstance(dest_cols, tuple) else ""
    if source_cols:
        final_table = table
        final_table_cols = dest_cols
        table = f"import_{table}"
        dest_cols = ""
        field_names = get_csv_field_names(f, encoding=encoding, delimiter=delimiter)
        op.create_table(
            table, *[sa.Column(c, sa.String) for c in map(str.lower, field_names)], schema=schema
        )

    options = ["FORMAT CSV"]
    if header:
        options.append("HEADER")
    if encoding:
        options.append(f"ENCODING '{encoding}'")
    if delimiter:
        options.append(f"DELIMITER E'{delimiter}'")
    options = ", ".join(options)
    cursor = op.get_bind().connection.cursor()
    cursor.copy_expert(
        f"""
        COPY {schema}.{table}{dest_cols}
        FROM STDIN WITH ({options})
    """,
        f,
    )

    if source_cols:
        source_cols = ", ".join(source_cols)
        op.execute(
            f"""
        INSERT INTO {schema}.{final_table}{final_table_cols}
          SELECT {source_cols}
            FROM {schema}.{table};
        """
        )
        op.drop_table(table, schema=schema)


def get_csv_field_names(f, encoding, delimiter):
    if encoding == "WIN1252":  # postgresql encoding
        encoding = "cp1252"  # python encoding
    reader = DictReader(f, delimiter=delimiter)
    field_names = reader.fieldnames
    f.seek(0)
    return field_names
