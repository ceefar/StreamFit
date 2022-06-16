# ---- IMPORTS ---- 
# for db
import pymysql
import os
from dotenv import load_dotenv
# for csv
import csv
# for filling equipment/exercise db tables
import integration_scrape_exrx as fitdb
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



# ---- START EQUIPMENT EXERCISES DB SETUP ----


def get_all_equip_for_mg(mg):

    print(f"{mg = }")
    if mg == "Chest":
        table_name = "chest_main"
    
    get_equip_query = f"SELECT DISTINCT mainEquip FROM {table_name}"
    equip_tuple = get_from_db(get_equip_query)

    print(f"{equip_tuple = }")
    print(f"{equip_tuple[0] = }")



def create_all_chest_tables():
    """ allows to go through web scrapped data and manually configure tables with ease """
    chest_data = fitdb.get_all_exercises_from_mg_chest()

    current_main_mg = "Chest-Main"
    current_main_equip = "Assisted"
    table_name = 'chest_main'

    for exercise in chest_data:
        print("\n\n")
        print(f"MG : {current_main_mg}, EQUIP : {current_main_equip}")
        print(f"NAME : {exercise[0]}, LINK : {exercise[1]}")

        user_select = int(input("\n[ 1 ] -  Add/Skip Item\n[ 2 ] -  Do Other (Update MG, Equip, Table)\nYour Selection : ")) # should have drop and quit for debug but meh, also could have end, view all, update etc but for now is fine
        
        if user_select == 2:
            while True:
                
                user_select = int(input("[ 1 ] -  Create New Table\n[ 2 ] -  Update Main MG\n[ 3 ] -  Update Main Equip\n[ 0 ] - Zero To Quit\nYour Selection : ")) # should have drop and quit for debug but meh, also could have end, view all, update etc but for now is fine

                if user_select == 0:
                    break

                if user_select == 1:
                    table_name = input("Enter Table Name : ")
                    create_new_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (exName VARCHAR(255), mainMuscle VARCHAR(255), exParent VARCHAR(255), mainEquip VARCHAR(255), equipAttach VARCHAR(255), exUtility VARCHAR(255), exMechanics VARCHAR(255), exForce VARCHAR(255), mainMuscleSynergists VARCHAR(255), mainMuscleStabalisers VARCHAR(255), exLink VARCHAR(255))"
                    add_to_db(create_new_table_query)

                if user_select == 2:
                    current_main_mg = input(f"Current MG = {current_main_mg}, Enter New Name : ")

                if user_select == 3:
                    current_main_equip = input(f"Current Equip = {current_main_equip}, Enter New Name : ")
                
                if user_select == 0:
                    break

        print("\n\n")
        print(f"MG : {current_main_mg}, EQUIP : {current_main_equip}")
        print(f"NAME : {exercise[0]}, LINK : {exercise[1]}")
        user_select = int(input("\n[ 2 ] -  Add Item\n[ 3 ] -  Skip Item\nYour Selection : ")) # should have drop and quit for debug but meh, also could have end, view all, update etc but for now is fine

        print("")
        
        if user_select == 3:
                continue

        if user_select == 2:
                print(f"Name To Add = {exercise[0]}")
                print(f"MG To Add = {current_main_mg}")
                print(f"Equip To Add = {current_main_equip}")
                print(f"Link To Add = {exercise[1]}")
                print(f"Into Table = {table_name}")

                parentinput = input(f"Add Parent = ")
                attachinput = input(f"Add Attachment = ")

                add_exercise_query = f"INSERT INTO {table_name} (exName, mainMuscle, exParent, mainEquip, equipAttach, exLink) VALUES ('{exercise[0]}','{current_main_mg}','{parentinput}','{current_main_equip}','{attachinput}','{exercise[1]}')"
                add_to_db(add_exercise_query)
        

    # 100% WANT A IS_POPULAR TAG/FLAG (as col)

    # LOL - mgs dont change enum would have been decent?! - consider for first refactor and when doing all exercises
    # FUNNILY ENOUGH THIS COULD BE CREATED LIKE AN ADMIN PANEL WITH A GUI USING STREAMLIT TOO! (little mini mini project for future?! - would be an awesome addition to show employers)

    # so need an option to create new table as there are cut offs
    # need option to skip a field
    # when adding prompt before to add its parent (should really display list of all parents too and then just allow to select one cause spelling but meh)
    # need links to be full not this shit (have that field at the end end)
    # could add is base+compound but is easy enough to get with a query so meh
    # also need specifics (tho can web scrap them dynamically) for utility mechanics force main mg, 
    #       - main synergists(there are lots so will scrape the rest for outputs), main stabalisers
    #       - else can be scraped for display to user
    #       - so just add the needed fields, will only be adding in now semi-manually, equipment, attachment (if has), parent (if has)
    #       - auto fields, main mg, equipment, name (done), link (done) 



# ---- START EQUIPMENT EXERCISES DB SETUP ----



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
    get_prev_sessionid_query = f"SELECT sessionid FROM {user_name}_sessions ORDER BY sessionid DESC LIMIT 1"
    prev_sessionid = get_from_db(get_prev_sessionid_query)
    prev_sessionid = prev_sessionid[0][0]
    prev_sessionid = int(prev_sessionid)
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
    get_previous_set_query = f"SELECT SetNumb, SetReps, SetWeight, SetTotalWeight FROM {user_name}_sessions WHERE sessionName = '{sessionName}' AND muscleNumbGroup = '{muscleNumb}' AND sessionid = '{prevSessionID}'"
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
    #create_all_chest_tables()
    main()

# ---- END DRIVER ----



# ---- BE LAZY ----

# print(f"{variable_name = }")
# print(f"{type(variable_name) = }")


# ---- QUERIES IM TOO SCARED TO DELETE LOL ----
# SELECT sessionid, setnumb FROM user_sessions ORDER BY sessionid DESC LIMIT 1