# ---- IMPORTS ---- 
# for db
import pymysql
import os
from dotenv import load_dotenv
# for csv
import csv
# ---- END IMPORTS ----



# ---- DATABASE INIT ----

# load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# establishes the database connection from .env file
connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    database = database
)

def add_to_db(command):
    """ adds values to the db with no return value, based on the given command (query) """
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    connection.commit()
    cursor.close()

def get_from_db(command):
    """ gets a result from the db, based on the given command (query) """
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    myresult = cursor.fetchall()
    connection.commit()
    cursor.close()
    return(myresult)

def close_connection():
    connection.close()

# ---- END DATABASE INIT ----



# ---- BASE DATABASE SETUP ----

def create_userdata_table(user_name:str = "user"):
    """ creates the base data table for the user if one doesn't exist, uses default 'user' if one is not provided"""
    table_existence = check_if_table_exists(user_name)
    if table_existence == "Exists":
        print(f"OH YEAH! - Table **{user_name}** Exists")
    elif table_existence == "NotFound":
        print(f"UH OH! - Table {user_name} Not Found, Creating It Now")
        create_base_table_query = f"CREATE TABLE IF NOT EXISTS {user_name} (userName VARCHAR(255), userID VARCHAR(255), SessionID VARCHAR(255))"
        add_to_db(create_base_table_query)
        print(f"THIS WAS A TRIUMPH! - Table **{user_name}** Created")
    elif table_existence == "NoParam":
        print("NOTICE - No Table Name Was Given")
    else:
        print("ERROR - Unplanned Error")

def check_if_table_exists(table_name:str = "") -> str:
    """ currently used for printing back if table existed prior but will expand in future, returns true if table is found """
    if table_name:
        check_if_table_exists_query = f"SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES WHERE TABLE_SCHEMA LIKE 'fit' AND TABLE_NAME = '{table_name}'"
        check_if_table_exists = get_from_db(check_if_table_exists_query)
        # return the result for execution and print to terminal
        if check_if_table_exists:
            return("Exists")
        else:
            return("NotFound")
    else:
        return("NoParam")

def get_all_tables() -> list:
    """ return a list of all the current table names in the database """
    get_all_tables_query = f"SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES WHERE TABLE_SCHEMA LIKE 'fit'"
    all_tables = get_from_db(get_all_tables_query)
    all_tables_list = []
    [all_tables_list.append(table[1]) for table in all_tables]
    return(all_tables_list)

def drop_tables(table_to_drop:str = "", wanna_drop:bool = False):
    """ by default function is off, turn on wanna_drop flag to execute
        used for creating new columns for tables and general debugging, defaults to drop all tables, unless table_to_drop is given """
    if wanna_drop:
        if table_to_drop: 
            drop_table_query = f"DROP TABLE {table_to_drop}"
            add_to_db(drop_table_query)
        else:
            list_of_all_tables = get_all_tables()
            [f"'{table}'" for table in list_of_all_tables]
            all_tables_for_query = ', '.join(list_of_all_tables)
            drop_tables_query = f"DROP TABLE {all_tables_for_query}"
            add_to_db(drop_tables_query)
    else:
        print("No Tables Were Harmed In The Execution Of This Function")

# ---- END BASE DATABASE SETUP ----



# ---- WORKOUT SESSION DB SETUP ----

def create_usersession_table(user_name:str = "user"):
    """ creates the user session data table for the user if one doesn't exist, uses default 'user' if one is not provided"""
    table_existence = check_if_usersession_table_exists(user_name)
    if table_existence == "Exists":
        print(f"OH YEAH! - Table **{user_name}** Exists")
    elif table_existence == "NotFound":
        print(f"UH OH! - Table {user_name} Not Found, Creating It Now")
        create_base_table_query = f"CREATE TABLE IF NOT EXISTS {user_name}_sessions (userID VARCHAR(255), SessionID VARCHAR(255), SessionName VARCHAR(255), MuscleNumbGroup VARCHAR(255), SetNumb INT, SetReps INT, SetWeight DECIMAL(6,2), SetTotalWeight DECIMAL(8,2), setRest INT)"
        add_to_db(create_base_table_query)
        print(f"THIS WAS A TRIUMPH! - Table **{user_name}** Created")
    elif table_existence == "NoParam":
        print("NOTICE - No Table Name Was Given")
    else:
        print("ERROR - Unplanned Error")


def check_if_usersession_table_exists(user_name:str = "") -> str:
    """ currently used for printing back if table existed prior but will expand in future, returns true if table is found """
    if user_name:
        check_if_table_exists_query = f"SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES WHERE TABLE_SCHEMA LIKE 'fit' AND TABLE_NAME = '{user_name}_sessions'" #user_sessions
        check_if_table_exists = get_from_db(check_if_table_exists_query)
        # return the result for execution and print to terminal
        if check_if_table_exists:
            return("Exists")
        else:
            return("NotFound")
    else:
        return("NoParam")


# ---- END WORKOUT SESSION DB SETUP ----


# ---- INTEGRATIONS TEST 1 ----

def db_create_user(user_name):
    print(f"\nRUN - DB CREATION - {user_name}")
    create_userdata_table(user_name)
    create_usersession_table(user_name)


def add_exercise_set_data_to_db(user_name, sessionName, muscleNumb, setNumb, setReps, setWeight, setTotalWeight, setRest):
    add_exercise_set_data_query = f"INSERT INTO {user_name}_sessions (userID, SessionID, SessionName, MuscleNumbGroup, SetNumb, SetReps, SetWeight, SetTotalWeight, setRest) VALUES ('{user_name}', '1', '{sessionName}', '{muscleNumb}', {setNumb}, {setReps}, {setWeight}, {setTotalWeight}, {setRest})"
    add_to_db(add_exercise_set_data_query)
    print(f"{user_name} - Set {setNumb} Written For {muscleNumb}")


# ---- MAIN ----

def main():
    user_name = "user"
    print("\nRUN - DB INTEGRATION")
    # for debug - drops all by default btw
    drop_tables(wanna_drop=False)
    # onboarding will go here
    create_userdata_table(user_name)
    create_usersession_table(user_name)
    
# ---- END MAIN ----



# ---- DRIVER ----

# driver... vrmmmm
if __name__=='__main__':
    main()

# ---- END DRIVER ----



# ---- BE LAZY ----

# print(f"{variable_name = }")
# print(f"{type(variable_name) = }")