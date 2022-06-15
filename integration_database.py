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


def add_exercise_set_data_to_db(user_name, sessionID, sessionName, muscleNumb, setNumb, setReps, setWeight, setTotalWeight, setRest):
    """" self referencing af """
    add_exercise_set_data_query = f"INSERT INTO {user_name}_sessions (userID, SessionID, SessionName, MuscleNumbGroup, SetNumb, SetReps, SetWeight, SetTotalWeight, setRest) VALUES ('{user_name}', '{sessionID}', '{sessionName}', '{muscleNumb}', {setNumb}, {setReps}, {setWeight}, {setTotalWeight}, {setRest})"
    add_to_db(add_exercise_set_data_query)
    print(f"{user_name} - Set {setNumb} Written For {muscleNumb}")


def get_previous_sessionid_and_return_current(user_name):
    """ RENAME THIS WTF JESUS MAN, it doesnt actually get the previous so dont say that, get the previous session id by using the username, really need to make this an int tho """
    get_prev_sessionid_query = f"SELECT sessionid, setnumb FROM {user_name}_sessions ORDER BY sessionid DESC LIMIT 1"
    prev_sessionid = get_from_db(get_prev_sessionid_query)
    prev_sessionid = prev_sessionid[0][0]
    prev_sessionid = int(prev_sessionid) + 1
    return(prev_sessionid)


def get_last_sessionid_from_current(user_name):
    """ get the previous session id by using the username """
    get_prev_sessionid_query = f"SELECT sessionid, setnumb FROM {user_name}_sessions ORDER BY sessionid DESC LIMIT 1"
    prev_sessionid = get_from_db(get_prev_sessionid_query)
    prev_sessionid = prev_sessionid[0][0]
    prev_sessionid = int(prev_sessionid) - 1
    return(prev_sessionid)


def find_previous_sets_for_muscle(user_name:str, sessionName:str, muscleNumb:str) -> tuple:
    """
    find previous performed set by the user for the given muscle group 
    obvs just poc as needs to be for equipment/exercise specific not muscle specific
    logic wont change much once equipment is implemented since exercise names are/will be unique
    """
    # could grab prev session id from existing function using username - tbf could just pass it tho lol
    # dont actually need this, can just grab the last ig anyway by ordering by this col and not returning/using the value for the col
    # add timestamp, makes this easier - then id can truly be an id too
    # keeping this tho actually as just makes it easier, sure if always 3 sets np, but with increasing set counts would become problematic 
    prevSessionID = get_last_sessionid_from_current(user_name)
    # print(f"{prevSessionID = }")
    # print(f"{sessionName = }")
    # print(f"{muscleNumb = }")
    get_previous_set_query = f"SELECT SetNumb, SetReps, SetWeight, SetTotalWeight FROM user_sessions WHERE sessionName = '{sessionName}' AND muscleNumbGroup = '{muscleNumb}' AND sessionid = '{prevSessionID}'"
    previous_set = get_from_db(get_previous_set_query)
    print(f"{previous_set = }")
    return(previous_set)



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