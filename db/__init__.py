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

def add_item(db_config, item):
    """
    Add a new item to the items table.
    """
    query = f"""
        INSERT INTO tooted (nimi, staatus, laius, pikkus, created_at)
        VALUES ( '{escape_string(item[0])}', '{escape_string(item[1])}', '{escape_string(item[2])}', '{escape_string(item[3])}', NOW())
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Item {item[0]} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding item: {e}")
    finally:
        if connection:
            connection.close()


def get_item(db_config, item_id):
    """
    Fetch a specific item from the items table.
    """
    query = f"""
        SELECT *
        FROM tooted
        WHERE idnum = '{escape_string(item_id)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching item: {e}")
    finally:
        if connection:
            connection.close()

def update_item(db_config, item):
    """
    Update an existing item in the items table.
    """
    query = f"""
        UPDATE tooted
        SET nimi = '{escape_string(item[1])}',
            staatus = '{escape_string(item[2])}',
            laius = '{escape_string(item[3])}',
            pikkus = '{escape_string(item[4])}'
        WHERE idnum = '{escape_string(str(item[0]))}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error while updating item: {e}")
    finally:
        if connection:
            connection.close()


def delete_item(db_config, item_id):
    """
    Delete an item from the items table.
    """
    query = f"""
        DELETE FROM tooted
        WHERE idnum = '{escape_string(str(item_id))}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Item {item_id} deleted successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while deleting item: {e}")
    finally:
        if connection:
            connection.close()

def get_all_asukohad(db_config):
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

def get_asukoht(db_config, asukoht_id):
    """
    Fetch a specific asukoht from the asukohad table.
    """
    query = f"""
        SELECT *
        FROM asukohad
        WHERE idnum = '{escape_string(asukoht_id)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching asukoht: {e}")
    finally:
        if connection:
            connection.close()

def add_asukoht(db_config, asukoht):
    """
    Add a new asukoht to the asukohad table.
    """
    query = f"""
        INSERT INTO asukohad ( kood, laius, pikkus)
        VALUES ('{escape_string(asukoht[0])}', '{escape_string(asukoht[1])}', '{escape_string(asukoht[2])}')
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Asukoht {asukoht[0]} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding asukoht: {e}")
    finally:
        if connection:
            connection.close()

def update_asukoht(db_config, asukoht):
    """
    Update an existing asukoht in the asukohad table.
    """
    query = f"""
        UPDATE asukohad
        SET kood = '{escape_string(asukoht[1])}',
            laius = '{escape_string(asukoht[2])}',
            pikkus = '{escape_string(asukoht[3])}'
        WHERE idnum = '{escape_string(str(asukoht[0]))}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error while updating asukoht: {e}")
    finally:
        if connection:
            connection.close()

def delete_asukoht(db_config, asukoht_id):
    """
    Delete an asukoht from the asukohad table.
    """
    query = f"""
        DELETE FROM asukohad
        WHERE idnum = '{escape_string(str(asukoht_id))}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error while deleting asukoht: {e}")
    finally:
        if connection:
            connection.close()

def get_all_transfers(db_config):
    """
    Fetch all transfers from the transfers table.
    """
    query = """
        SELECT *
        FROM transferid
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching transfers: {e}")
    finally:
        if connection:
            connection.close()

def add_transfer(db_config, transfer):
    """
    Add a new transfer to the transfers table.
    """
    query = f"""
        INSERT INTO transferid (user, created_date, staatus, aadress, tyyp)
        VALUES ('{escape_string(transfer[0])}', '{escape_string(transfer[1])}', '{escape_string(transfer[2])}', '{escape_string(transfer[3])}', '{escape_string(transfer[4])}')
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Transfer {transfer[0]} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding transfer: {e}")
    finally:
        if connection:
            connection.close()

def get_transfer(db_config, transfer_id):
    """
    Fetch a specific transfer from the transfers table.
    """
    query = f"""
        SELECT *
        FROM transferid
        WHERE idnum = '{escape_string(transfer_id)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching transfer: {e}")
    finally:
        if connection:
            connection.close()

def add_transfer_line(db_config, transfer_line):
    """
    Add a new transfer line to the transfer_lines table.
    """
    query = f"""
        INSERT INTO transfer_read (trans_id, item, qty)
        VALUES ('{escape_string(transfer_line[0])}', '{escape_string(transfer_line[1])}', '{escape_string(transfer_line[2])}')
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Transfer line {transfer_line[0]} added successfully.")
    except pymysql.MySQLError as e:
        print(f"Error while adding transfer line: {e}")
    finally:
        if connection:
            connection.close()

def get_last_transfer_id(db_config):
    """
    Fetch the last transfer ID from the transfers table.
    """
    query = """
        SELECT MAX(idnum) FROM transferid
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None
    except pymysql.MySQLError as e:
        print(f"Error while fetching last transfer ID: {e}")
    finally:
        if connection:
            connection.close()

def get_transfer_lines(db_config, transfer_id):
    """
    Fetch all transfer lines for a specific transfer.
    """
    query = f"""
        SELECT  tr.idnum, tr.trans_id, tr.item, tr.qty, tooted.nimi
        FROM transfer_read as tr left join tooted on tr.item = tooted.idnum
        WHERE tr.trans_id = '{escape_string(transfer_id)}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"Error while fetching transfer lines: {e}")
    finally:
        if connection:
            connection.close()

def update_transfer(db_config, transfer):
    """
    Update an existing transfer in the transfers table.
    """
    query = f"""
        UPDATE transferid
        SET created_date = '{escape_string(transfer[1])}',
            staatus = '{escape_string(transfer[2])}',
            aadress = '{escape_string(transfer[3])}',
            tyyp = '{escape_string(transfer[4])}'
        WHERE idnum = '{escape_string(str(transfer[0]))}'
    """
    connection = get_connection(db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error while updating transfer: {e}")
    finally:
        if connection:
            connection.close()



if __name__ == "__main__":
    pass