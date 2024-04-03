import pymysql as mysql


def connect_mysql(host:str, user:str, password:str):
    """ Establece una conexión con un servidor MySQL.

    Returns:
        connection(pymysql.Connection): Un objeto de conexión a la base de datos MySQL.
    """
    return mysql.connect(host=host, user=user, password=password)


def mysql_query(connection, query:str):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()  # Obtener todos los resultados de la consulta
        return result


def get_mysql_dbs(connection):
    """ Recupera los nombres de todas las bases de datos en un servidor MySQL,
    excluyendo las bases de datos del sistema.

    Returns:
        list: Lista de nombres de las bases de datos.
    """
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES WHERE `Database` NOT IN ('mysql', 'performance_schema', 'sys', 'information_schema')")
        return [db[0] for db in cursor.fetchall()]


def create_mysql_db(connection, database:str):
    """ Crea una nueva base de datos en un servidor MySQL si la base de datos no existe ya.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")


def check_mysql_db_exist(connection, database:str):
    """ Verifica si una base de datos específica existe en un servidor MySQL.

    Returns:
        bool: Verdadero si la base de datos existe, falso en caso contrario.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{database}'")
        return cursor.fetchone() is not None


def close_mysql_conn(connection):
    connection.close()