from tkinter import messagebox


def convert_data_type(sqls_data_type:str):
    """ Convierte los tipos de datos de SQL Server a los tipos de datos equivalentes de MySQL.

    Returns:
        str: Datos equivalente en MySQL. Si el tipo de datos de SQL Server no está en el mapeo, se devuelve 'VARCHAR' por defecto.
    """
    data_type_mapping = {
        "int": "INT", "bigint": "BIGINT", "smallint": "SMALLINT", "tinyint": "TINYINT", "bit": "BOOLEAN",
        "float": "FLOAT", "real": "FLOAT", "decimal": "DECIMAL", "numeric": "NUMERIC", "smallmoney": "DECIMAL",
        "money": "DECIMAL", "datetime": "DATETIME", "smalldatetime": "DATETIME", "date": "DATE", "time": "TIME",
        "char": "CHAR", "varchar": "VARCHAR", "text": "TEXT", "nvarchar": "VARCHAR", "ntext": "LONGTEXT",
        "binary": "BINARY", "varbinary": "VARBINARY", "image": "LONGBLOB", "xml": "LONGTEXT"
    }
    return data_type_mapping.get(sqls_data_type.lower(), "VARCHAR")


def convert_sql_server_to_mysql_data_types(sqls_columns:list):
    """ Convierte los tipos de datos de las columnas de SQL Server a los tipos de datos equivalentes de MySQL.

    Returns:
        list: Lista de tuplas, donde cada tupla contiene el nombre de la columna, el tipo de datos equivalente en MySQL y la longitud de los datos.
    """
    return [(column_name, convert_data_type(sql_server_data_type), data_length)
            for column_name, sql_server_data_type, data_length in sqls_columns]


def get_sql_server_tables(connection, database:str):
    """ Recupera los nombres de todas las tablas en una base de datos específica de SQL Server.

    Returns:
        list: Lista de nombres de tablas.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"USE {database}")
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME NOT LIKE '%#'")
        return [table[0] for table in cursor.fetchall()]


def get_mysql_tables(connection, database:str):
    """ Recupera los nombres de todas las tablas en una base de datos específica de MySQL que no son vistas.

    Returns:
        list: Lista de nombres de tablas.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"USE {database}")
        cursor.execute("SHOW FULL TABLES WHERE TABLE_TYPE != 'VIEW'")
        return [table[0] for table in cursor.fetchall()]


def get_sql_server_table_structure(connection, table:str):
    """ Recupera la estructura de una tabla específica en SQL Server. La estructura incluye los nombres de las columnas, los tipos de datos y la longitud máxima de los caracteres. También recupera las claves primarias y las claves foráneas de la tabla.

    Returns:
        tuple: Tupla que contiene tres listas. La primera contiene las columnas de la tabla, La segunda lista contiene las claves primarias, y La tercera las claves foráneas de la tabla.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH "
                       f"FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}'")
        columns = [(column_name, data_type, character_maximum_length)
                   for column_name, data_type, character_maximum_length in cursor.fetchall()]
        primary_keys = get_sql_server_primary_keys(connection, table)
        foreign_keys = get_sql_server_foreign_keys(connection, table)
    return columns, primary_keys, foreign_keys


def get_sql_server_primary_keys(connection, table:str):
    """ Recupera los nombres de todas las claves primarias de una tabla específica en SQL Server.

    Returns:
        list: Lista de nombres de claves primarias.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
                       f"WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1 "
                       f"AND TABLE_NAME='{table}'")
        return [row[0] for row in cursor.fetchall()]


def get_sql_server_foreign_keys(connection, table:str):
    """ Recupera las claves foráneas de una tabla específica en SQL Server. Para cada clave foránea, se recupera el nombre de la tabla, el nombre de la columna, el nombre de la tabla referenciada y el nombre de la columna referenciada.

    Returns:
        list: Lista de tuplas. Cada tupla contiene el nombre de la tabla, el nombre de la columna, el nombre de la tabla referenciada y el nombre de la columna referenciada.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT OBJECT_NAME(parent_object_id) AS TableName, c1.name AS ColumnName, "
            f"OBJECT_NAME(referenced_object_id) AS ReferencedTableName, c2.name AS ReferencedColumnName "
            f"FROM sys.foreign_key_columns fkc "
            f"INNER JOIN sys.columns c1 ON fkc.parent_object_id = c1.object_id AND fkc.parent_column_id = c1.column_id "
            f"INNER JOIN sys.columns c2 ON fkc.referenced_object_id = c2.object_id AND fkc.referenced_column_id = c2.column_id "
            f"WHERE OBJECT_NAME(parent_object_id) = '{table}'"
        )
        return cursor.fetchall() or []


def add_foreign_keys_to_table(connection, table:str, foreign_keys:list):
    """ Agrega claves foráneas a una tabla específica en una base de datos MySQL. Para cada clave foránea, se crea una consulta ALTER TABLE y se ejecuta.
    """
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


def create_mysql_table(connection, database:str, table:str, columns:list, primary_key:list):
    """ Crea una tabla en una base de datos MySQL específica si la tabla no existe ya. La estructura de la tabla se define mediante los nombres de las columnas, los tipos de datos y la longitud de los datos. También se puede definir una clave primaria para la tabla.
    """
    create_table_query = f"CREATE TABLE IF NOT EXISTS {database}.{table} ("
    for column in columns:
        column_name, data_type, data_length = column
        create_table_query += f"{column_name} {data_type}"
        if data_length:
            create_table_query += f"({data_length})"
        create_table_query += ", "
    if primary_key:
        create_table_query += f"PRIMARY KEY ({', '.join(primary_key)}), "
    create_table_query = create_table_query.rstrip(", ") + ")"
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
    connection.commit()


def transfer_data(sqls_conn, mysql_conn, database:str, table:str, columns:list):
    """ Transfiere los datos de una tabla específica de SQL Server a una tabla en MySQL. Los datos se recuperan de la tabla de SQL Server y luego se insertan en la tabla de MySQL.
    """
    with sqls_conn.cursor() as source_cursor, mysql_conn.cursor() as dest_cursor:
        source_cursor.execute(f"SELECT * FROM {table}")
        data = source_cursor.fetchall()
        for row in data:
            values = [value if value is not None else None for value in row]
            placeholders = ", ".join(["%s" for _ in range(len(values))])
            insert_query = f"INSERT INTO {database}.{table} VALUES ({placeholders})"
            dest_cursor.execute(insert_query, values)
        mysql_conn.commit()


def migrate_db_to_mysql(sqls_conn, mysql_conn, database:str, tables):
    """ Migra una base de datos completa de SQL Server a MySQL. Recupera las tablas de la base de datos de SQL Server, luego para cada tabla, recupera su estructura, convierte los tipos de datos de SQL Server a los tipos de datos equivalentes de MySQL, crea la tabla en MySQL y transfiere los datos.
    """
    if tables:
        sqls_tables = tables
    else:
        sqls_tables = get_sql_server_tables(sqls_conn, database)

    for table in sqls_tables:
        try:
            print(f"┕> Transfiriendo tabla: {table}")
            columns, primary_key, _ = get_sql_server_table_structure(sqls_conn, table)
            new_structure = convert_sql_server_to_mysql_data_types(columns)
            create_mysql_table(mysql_conn, database, table, new_structure, primary_key)
            transfer_data(sqls_conn, mysql_conn, database, table, new_structure)
        except Exception as e:
            print(f"Error al migrar la tabla {table}: {e}")


def add_foreign_keys(sqls_conn, mysql_conn, database:str):
    """ Agrega claves foráneas a todas las tablas en una base de datos MySQL específica. Para cada tabla, recupera las claves foráneas de la tabla correspondiente en SQL Server y luego las agrega a la tabla en MySQL.
    """

    mysql_tables = get_mysql_tables(mysql_conn, database)
    
    for table in mysql_tables:
        try:
            print(f"┕> Transfiriendo llaves foraneas a la tabla: {table}")
            _, _, foreign_keys = get_sql_server_table_structure(sqls_conn, table)
            add_foreign_keys_to_table(mysql_conn, table, foreign_keys)
        except Exception as e:
            print(f"Error al agregar claves foráneas a la tabla {table}: {e}")


def migrate_to_mysql_process(sqls_conn, mysql_conn, database, tables):
    """Proceso de migracion una base de datos SQL Server a MySQL
    """
    try:
        migrate_db_to_mysql(sqls_conn, mysql_conn, database, tables)
        add_foreign_keys(sqls_conn, mysql_conn, database)
        print("Migración completada con éxito.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")