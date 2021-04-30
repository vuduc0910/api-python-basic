import sqlite3
db = sqlite3.connect("../users.db")
cursor = db.cursor()

try:
    query_db = "CREATE TABLE users(name nvarchar(30) PRIMARY KEY," \
               "password nvarchar(16) NOT NULL," \
               "email varchar(50) NOT NULL)"
    cursor.execute(query_db)
except:
    pass


def create_query_insert(name, password, email):
    query_insert = "INSERT INTO users VALUES('"+name+"','"+password+"','"+email+"')"
    cursor.execute(query_insert)
    db.commit()
    return '200'


def create_query_update(name, password, email):
    query_update = "UPDATE users SET password = '"+password+"',email = '"+email+"' WHERE name = '"+name+"'"
    cursor.execute(query_update)
    db.commit()
    return '200'


def create_query_delete(name):
    query_delete = "DELETE FROM users WHERE name = '"+name+"'"
    cursor.execute(query_delete)
    db.commit()
    return '200'


def create_query_get(name):
    query_select = "SELECT * FROM users where name ='"+ name +"'"
    list_users = []
    for row in cursor.execute(query_select):
        user = {'name': row[0], 'password': row[1], 'email': row[2]}
        list_users.append(user)
    return list_users


if __name__ == '__main__':
    pass