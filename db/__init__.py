import pymysql
from pymysql.converters import escape_string

def get_connection(db_config):
    """
    Establish a connection to the MySQL database.
    """
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")  # Debug
        raise


def execute_query(db_config, query):
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

        with connection.cursor() as cursor:
            print(f"Executing Query: {query}")  # Debug
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Query Result: {result}")  # Debug
            return result

    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")  # Debug
        raise

    finally:
        if connection:
            connection.close()
            print("MySQL connection closed")


def get_asukohad(db_config):
    """
    Fetch all asukohad from the asukohad table.
    """
    query = """
        SELECT *
        FROM asukohad
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching asukohad: {e}")
    finally:
        if connection:
            connection.close()

def get_users(db_config):
    """
    Fetch all users from the users table.
    """
    query = """
        SELECT *
        FROM users
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching users: {e}")
    finally:
        if connection:
            connection.close()

def add_user(db_config, username, password):
    """
    Add a new user to the users table.
    """
    query = f"""
        INSERT INTO users (username, passhash)
        VALUES ('{escape_string(username)}', '{escape_string(password)}')
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"User {username} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding user: {e}")
    finally:
        if connection:
            connection.close()


def get_load(db_config):
    """
    Fetch all load from the load table.
    """
    query = """
        SELECT *
        FROM lubad
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching load: {e}")
    finally:
        if connection:
            connection.close()

def get_userload(db_config, username):
    """
    Fetch all load for a specific user.
    """
    query = f"""
        SELECT *
        FROM userload
        WHERE username = '{escape_string(username)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching user load: {e}")
    finally:
        if connection:
            connection.close()

def del_userloads(db_config, username):
    """
    Delete user loads in the database.
    """
    query= f"""
        DELETE FROM userload
        WHERE username = '{escape_string(username)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"User loads for {username} deleted successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while deleting user loads: {e}")
    finally:
        if connection:
            connection.close()

def add_userloads(db_config, loads):

    for load in loads:
        add_userload(db_config, load)

def add_userload(db_config, load):
    """
    Add new user loads to the database.
    """
    query = f"""
        INSERT INTO userload (username, luba)
        VALUES ('{escape_string(load[0])}', '{escape_string(load[1])}')
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"User load {load[1]} for {load[0]} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding user load: {e}")
    finally:
        if connection:
            connection.close()

def get_all_items(db_config):
    """
    Fetch all items from the items table.
    """
    query = """
        SELECT *
        FROM tooted
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching items: {e}")
    finally:
        if connection:
            connection.close()



if __name__ == "__main__":
    pass