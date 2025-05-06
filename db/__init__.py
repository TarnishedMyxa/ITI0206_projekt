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



if __name__ == "__main__":
    pass