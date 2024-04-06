from tkinter import messagebox


def convert_data_type(mysql_data_type):
    data_type_mapping = {
        "INT": "int", "BIGINT": "bigint", "SMALLINT": "smallint", "TINYINT": "tinyint",
        "BOOLEAN": "bit", "FLOAT": "float", "DECIMAL": "decimal", "NUMERIC": "numeric",
        "DATETIME": "datetime", "DATE": "date", "TIME": "time", "CHAR": "char",
        "VARCHAR": "varchar(255)", "TEXT": "text", "LONGTEXT": "ntext", "BINARY": "binary",
        "VARBINARY": "varbinary", "LONGBLOB": "image",
    }
    return data_type_mapping.get(mysql_data_type.upper(), "VARCHAR(255)")


def convert_mysql_to_sql_server_data_types(mysql_columns):
    return [(col_name, convert_data_type(col_type), data_length) for col_name, col_type, data_length in mysql_columns]


def get_sql_server_tables(connection, database):
    with connection.cursor() as cursor:
        cursor.execute(f"USE {database}")
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME NOT LIKE '%#'")
        return [table[0] for table in cursor.fetchall()]


def get_mysql_tables(connection, database):
    with connection.cursor() as cursor:
        cursor.execute(f"USE {database}")
        cursor.execute("SHOW FULL TABLES WHERE TABLE_TYPE != 'VIEW'")
        return [table[0] for table in cursor.fetchall()]


def get_mysql_table_structure(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [(row[0], row[1], None) for row in cursor.fetchall()]
        primary_keys = get_mysql_primary_keys(connection, table)
        foreign_keys = get_mysql_foreign_keys(connection, table)
    return columns, primary_keys, foreign_keys


def get_mysql_primary_keys(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
                       f"WHERE TABLE_SCHEMA = DATABASE() AND CONSTRAINT_NAME = 'PRIMARY' "
                       f"AND TABLE_NAME='{table}'")
        return [row[0] for row in cursor.fetchall()]


def get_mysql_foreign_keys(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT TABLE_NAME AS TableName, COLUMN_NAME AS ColumnName, "
            f"REFERENCED_TABLE_NAME AS ReferencedTableName, REFERENCED_COLUMN_NAME AS ReferencedColumnName "
            f"FROM information_schema.key_column_usage "
            f"WHERE TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL"
        )
        return cursor.fetchall() or []


def add_foreign_keys_to_table(connection, table, foreign_keys):
    with connection.cursor() as cursor:
        for i, fk in enumerate(foreign_keys, start=1):
            referenced_table, column_name, referenced_table_name, referenced_column_name = fk
            fk_name = f"FK_{table}_{referenced_table_name}"
            alter_table_query = (
                f"ALTER TABLE {table} "
                f"ADD CONSTRAINT {fk_name} "
                f"FOREIGN KEY ({column_name}) "
                f"REFERENCES {referenced_table_name}({referenced_column_name})"
            )
            cursor.execute(alter_table_query)
    connection.commit()


def create_sql_server_table(connection, selected_db, table_name, columns, primary_key):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"USE {selected_db}")

        create_table_query = f"CREATE TABLE {table_name} ("
        for column in columns:
            column_name, data_type, data_length = column
            create_table_query += f"{column_name} {data_type}"
            if data_length:
                create_table_query += f"({data_length})"
            create_table_query += ", "
        if primary_key:
            primary_key_constraint = f"CONSTRAINT PK_{table_name} PRIMARY KEY ({', '.join(primary_key)})"
            create_table_query += primary_key_constraint
        create_table_query = create_table_query.rstrip(", ") + ")"
        
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
        connection.commit()
    except Exception as e:
        print(f"Error en la sintaxis de la consulta o al crear la tabla {table_name}: {e}")


def transfer_data(mysql_connection, sql_server_connection, selected_db, table_name, columns):
    with mysql_connection.cursor() as source_cursor, sql_server_connection.cursor() as dest_cursor:
        source_cursor.execute(f"SELECT * FROM {table_name}")
        data = source_cursor.fetchall()
        for row in data:
            values = [value if value is not None else None for value in row]
            placeholders = ", ".join(["?" for _ in range(len(values))])
            insert_query = (
                f"INSERT INTO {selected_db}.dbo.{table_name} VALUES ({placeholders})"
            )
            dest_cursor.execute(insert_query, values)
        sql_server_connection.commit()


def migrate_db_to_sql_server(sqls_conn, mysql_connn, database:str, tables):
    if tables:
        mysql_tables = tables
    else:
        mysql_tables = get_mysql_tables(mysql_connn, database)

    for table in mysql_tables:
        try:
            print(f"┕> Transfiriendo tabla: {table}")
            columns, primary_key, _ = get_mysql_table_structure(mysql_connn, table)
            new_strucutre = convert_mysql_to_sql_server_data_types(columns)
            create_sql_server_table(sqls_conn, database, table, new_strucutre, primary_key)
            transfer_data(mysql_connn, sqls_conn, database, table, new_strucutre)
        except Exception as e:
            print(f"Error al migrar la tabla {table}: {e}")


def add_foreign_keys(sqls_conn, mysql_conn, database:str):

    sqls_tables = get_sql_server_tables(sqls_conn, database)

    for table in sqls_tables:
        try:
            print(f"┕> Transfiriendo llaves foraneas a la tabla: {table}")
            _, _, foreing_key = get_mysql_table_structure(mysql_conn, table)
            add_foreign_keys_to_table(sqls_conn, table, foreing_key)
        except Exception as e:
            print(f"Error al agregar claves foráneas a la tabla {table}: {e}")


def migrate_to_sql_server_process(sqls_conn, mysql_conn, database, tables):
    """Proceso de migracion una base de datos SQL Server a MySQL
    """
    try:
        migrate_db_to_sql_server(sqls_conn, mysql_conn, database, tables)
        add_foreign_keys(sqls_conn, mysql_conn, database)
        print("Migración completada con éxito.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")