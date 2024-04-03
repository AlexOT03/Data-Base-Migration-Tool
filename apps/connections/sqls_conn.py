import pyodbc as sql_server


def connect_sqls(driver:str, server:str, win_auth:bool, user:str, password:str):
    """ Establece una conexión con un servidor SQL Server.

    Returns:
        connection(pyodbc.Connection): Un objeto de conexión a la base de datos SQL Server.
    """
    if win_auth == '1':
        return sql_server.connect(driver=driver, server=server, trusted_connection="yes")
    else:
        return sql_server.connect(driver=driver, server=server, user=user, password=password)


def sqls_query(connection, query:str):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()  # Obtener todos los resultados de la consulta
        return result


def get_sqls_dbs(connection):
    """ Recupera los nombres de todas las bases de datos en un servidor SQL Server,
    excluyendo las primeras cuatro que son las bases de datos del sistema.

    Returns:
        list: Lista de nombres de las bases de datos.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")
        return [db[0] for db in cursor.fetchall()]
    

def create_sqls_db(connection, database):
    """ Crea una nueva base de datos en un servidor SQL Server si la base de datos no existe ya.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"IF DB_ID('{database}') IS NULL CREATE DATABASE {database}")


def check_sqls_db_exist(connection, database):
    """ Verifica si una base de datos específica existe en un servidor SQL Server.

    Returns:
        bool: Verdadero si la base de datos existe, falso en caso contrario.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{database}'")
        return cursor.fetchone() is not None


def close_sqls_conn(connection):
    connection.close()