from csv import list_dialects
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def createUser(conn, user):
    """
    Create a new user into the projects table
    :param conn:
    :param user:
    :return: id
    """
    sql = ''' INSERT INTO user(user_name, password, first_name, last_name)
              VALUES(?,?,?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def getUserId(conn, userName:str):
    with conn:
        sql = "SELECT id from user where user_name = ?"
        cur = conn.cursor()
        res = cur.execute(sql, (userName,))
        userId = cur.fetchone()
    return userId


def getUserLists(conn, userName:str):
    with conn:
        getListsQuery = "SELECT name from list where user_id = ?"
        getUserIdQuery = "select id from user where user_name = ?"
        cur = conn.cursor()
        res = cur.execute(getUserIdQuery, (userName,))
        userId = cur.fetchone()
        res = cur.execute(getListsQuery, userId)
        lists = cur.fetchall()
        for list in lists:
            print(list)

def create_list(conn, list):
    '''
    Create a new list in the list table
    param conn:
    param list:
    '''

    sql = ''' INSERT INTO list(name, user_id)
            VALUES (?, ?)
            '''
    cur = conn.cursor()
    cur.execute(sql, list)
    conn.commit()
    return cur.lastrowid


def addItemToList(conn, listName, upc, store, price):
    with conn:
        addItemQuery = "INSERT INTO item (upc, current_store, current_price, list_id)\
            VALUES (?, ?, ?, ?)"
        cur = conn.cursor()
        getListIdQuery = "SELECT id from list where name = ?"
        cur.execute(getListIdQuery, (listName,))
        listId = cur.fetchone()[0]
        print(listId)
        cur.execute(addItemQuery, (upc, store, price, listId))
        

def addListForUser(conn, listName, userId):
    try:
        create_list(conn, (listName, userId))
    except:
        print('error adding list')

def create_item(conn, item):
    '''
    '''
    sql = ''' INSERT INTO item (upc, current_store, current_price, list_id)
            VALUES (?, ?, ?, ?)
        '''
    cursor = conn.cursor()
    cursor.execute(sql, item)
    conn.commit()

def createData(database_name:str):
    database = database_name
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user(
                                    id INTEGER PRIMARY KEY,
                                    user_name TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    first_name TEXT,
                                    last_name TEXT,
                                    date_created DATETIME default current_timestamp,
                                    date_modified DATETIME
                                    ); """

    sql_create_list_table = """CREATE TABLE IF NOT EXISTS list (
                                    id INTEGER PRIMARY KEY,
                                    user_id INTEGER NOT NULL,
                                    name text NOT NULL,
                                    date_created DATETIME default current_timestamp,
                                    date_modified DATETIME,
                                    FOREIGN KEY (user_id) REFERENCES user (id)
                                );"""
    sql_create_item_table = """create table IF NOT EXISTS item (
                                    id integer PRIMARY KEY,
                                    list_id INTEGER NOT NULL,
                                    upc TEXT NOT NULL,
                                    current_store TEXT NOT NULL,
                                    current_price REAL
                                    date_created DATETIME default current_timestamp,
                                    date_modified DATETIME,
                                    FOREIGN KEY (list_id) REFERENCES list (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create user table
        create_table(conn, sql_create_user_table)

        # create list table
        create_table(conn, sql_create_list_table)

        # create item table
        create_table(conn, sql_create_item_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        # create a new user
        user = ('user1', 'password1', 'firstname1', 'lastname1');
        user_id = createUser(conn, user)
        # list
        list1 = ('list1', user_id)
        list2 = ('list2', user_id)
        # create lists
        list1_id = create_list(conn, list1)
        list2_id = create_list(conn, list2)
        # items
        item1 = ('upc1', 'store1', 6.7, list1_id)
        item2 = ('upc2', 'store1', 9.7, list1_id)
        item3 = ('upc1', 'store2', 12.7, list2_id)
        item4 = ('upc2', 'store2', 13.7, list2_id)
        # add items
        create_item(conn, item1)
        create_item(conn, item2)
        create_item(conn, item3)
        create_item(conn, item4)
        
if __name__ == '__main__':
    database_name = 'grocery_list.db'
    createData(database_name = database_name)
    conn = create_connection(database_name)
    print(getUserId(conn, 'user1'))
    getUserLists(conn, 'user1')
    addItemToList(conn, 'list1', 'upc1', 'walmart1', 2.5)