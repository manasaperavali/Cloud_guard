
import pymysql
import sys
from prettytable import PrettyTable
import hashlib

# pip install pymysql prettytable hashlib 

Host = "localhost"
User = "manager"

Password = "dummy"
Database = "medrecord"
login_data = False

connection = pymysql.connect(
    host=Host,
    user=User,
    password=Password,
    database=Database,
    cursorclass=pymysql.cursors.DictCursor
)

grouptype = []


def hash_string(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()


def home_menu():
    print("1 - Login")
    print("2 - Register")
    print("3 - Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        print("Goodbye")
        sys.exit()
    else:
        print("Invalid choice, please try again")
        home_menu()


def registeration(username, password, group):
    try:
        with connection.cursor() as cursor:
            new_row_data = {
                'username': username,
                'password': password,
                'groupname': group
            }

            sql = "INSERT INTO Userinfo ({}) VALUES ({})".format(
                ', '.join(new_row_data.keys()),
                ', '.join('%s' for _ in new_row_data)
            )

            cursor.execute(sql, tuple(new_row_data.values()))

        connection.commit()

        print("Register successfully, now login")
        home_menu()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
        connection.close()


def check_credentials(username, password):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Userinfo WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))

            result = cursor.fetchone()

            if result:
                print("Login successful!")
                login_data = True
                return True
            else:
                print("Invalid username or password.")
                return False
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
        connection.close()


def login_manage():
    print("your group is: " + grouptype[0])
    print("1 - Run query")
    print("2 - Logout")
    print("3 - Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        run_query()
    elif choice == "2":
        grouptype.pop()
        home_menu()
        login_data = False
    elif choice == "3":
        print("Goodbye")
        sys.exit()
    else:
        print("Invalid choice, please try again")
        print("here")
        login_manage()


def get_group_name(username, password):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT groupname FROM Userinfo WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()

            if result:
                group_name = result['groupname']
                grouptype.append(group_name)
                return group_name
            else:
                return None
    except Exception as e:
        print(f"Error: {e}")
        connection.close()


def run_query():
    query = input("Enter query: ")
    if (grouptype[0] == "R" and "insert" in query.lower()):
        print("Group R users don't have permission to insert data")
    elif (grouptype[0] == "H" and "insert" in query.lower()):
        query1 = query.lower().split("values(")
        query2 = query1[1].split(")")
        query3 = query2[0]
        query3 = query3.replace(' "', '')
        query3 = query3.replace('"', "")
        query4 = query3.split(",")
        first_name = query4[0]
        last_name = query4[1]
        gender = query4[2]
        age = query4[3]
        weigth = float(query4[4])
        heigth = float(query4[5])
        health_history = query[6]
        newquery = 'VALUES("'+hash_string(first_name)+' ,"'+hash_string(last_name)+' ,"'+hash_string(gender)+' ,"' + \
            hash_string(age)+' ,"'+hash_string(weigth)+' ,"' + \
            hash_string(heigth)+' ,"'+hash_string(health_history)+'"'
        main_query = query1[0] + newquery
        print(main_query)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                main_query = main_query.lower().replace("healthcare", "healthcare_hash")
                cursor.execute(main_query)
                connection.commit()
                print("Data inserted successfully.")

        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
            connection.close()

    elif "select" in query.lower():
        if (grouptype[0] == "R" and "first_name" in query.lower()):
            print("Group R users don't have permission to view first_name")
        elif (grouptype[0] == "R" and "last_name" in query.lower()):
            print("Group R users don't have permission to view last_name")
        else:
            if grouptype[0] == "R":
                if "*" in query:
                    query = query.replace(
                        "*", "id, gender, age, weight, height, health_history ")
                    print(query)

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    newquery = query.replace("healthcare", "healthcare_hash")
                    cursor.execute(newquery)
                    resutls2 = cursor.fetchall()
                    table = PrettyTable()
                    table.field_names = results[0].keys() if results else []

                    for i, (row, hash_row) in enumerate(zip(results, resutls2)):

                        table.add_row(row.values())
                        for key, value in row.items():

                            # if type(value) == float:
                            #     value = int(value)
                            #     print(value)
                            #     print("-------------------------")

                            manual_hash = hash_string(str(value))
                            existing_hash = hash_row.get(key, "")
                            if key == "id":
                                existing_hash = str(value)
                                manual_hash = existing_hash

                            if manual_hash == existing_hash:
                                pass
                            else:
                                print(f"Row {i+1}, column {key}")
                                print("Value: ", value)
                                
                                print("Manual hash: ", manual_hash)
                                print("Existing hash: ", existing_hash)
                                print("Hash mismatch!")
                                sys.exit()
                    print(table)

            except Exception as e:
                print(f"Error: {e}")
                connection.close()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if (check_credentials(username, password)):
        print("Welcome " + username)
        login_data = True
        group_name = get_group_name(username, password)
        while login_data:
            login_manage()
    else:
        home_menu()


def register():
    group_list = ["H", "R"]
    username = input("Enter username: ")
    password = input("Enter password:")
    group = ""
    while group not in group_list:
        group = input("Enter group type(H/R): ")
    registeration(username, password, group)


if __name__ == "__main__":
    home_menu()
