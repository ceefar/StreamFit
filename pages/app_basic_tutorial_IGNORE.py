# imports 
# for web app and test components
import streamlit as st
# for timing - changing this if you want to other better time but if fine for now
from time import sleep
# for images
from PIL import Image
# for folder search
import os
# integrations for db access, workout calculations 
import integration_database as fitdb
import integration_workout as wocalc
import integration_scrape_exrx as exrx
import screenshotter as sss #selenium screenshotter


# NEED TO DO BUT CBA RN FEEL TOO ROUGH URGH

#---- functions ----

def find_image_files():
    files = os.listdir('images')
    st.write(files)
    return(files)
    # NOTE: CAN LEGIT DO THE SESSION STATE STUFF IN THIS FUNCT!?!?!!
    #for file in files:
        

def set_muscle_just_name(muscle:str) -> str:
    if muscle == "Front":
        muscle_just_name = "Front Delt"
    else:
        muscle_just_name = muscle
    return(muscle_just_name)

@st.cache
def get_equip_list(muscle):
    exequip = fitdb.get_all_equip_for_mg(muscle)
    return(exequip)

def get_equipexercises_basic(equiplist):
    return(fitdb.get_equipexercises_forlist_basic(equiplist))

def split_current_equipex_name_for_link(equipex_name:str, muscle_justname:str) -> str:
    """ self referencing, returns link, should find an easier way to do this tho """
    # if is a child
    if "->" in equipex_name:
        kids_index = equipex_name.find("->")
        equip_index = equipex_name.find("[")
        kids_name = equipex_name[kids_index+3:equip_index-1]
        parents_name = equipex_name[:kids_index]
        equip_name = equipex_name[equip_index+1:-1]
        parents_name = parents_name.strip()
        exercise_link = use_name_get_link(muscle_justname, parents_name, equip_name, kids_name)
        return(exercise_link)
    else:
        # if its a parent (no child)
        equip_index = equipex_name.find("[")
        equip_name = equipex_name[equip_index+1:-1]
        parents_name = equipex_name[:equip_index]
        parents_name = parents_name.strip()
        # st.write(f"{parents_name = }")
        # st.write(f"{equip_name = }")
        exercise_link = use_name_get_link(muscle_justname, parents_name, equip_name)
        return(exercise_link)

def use_name_get_link(musclegroup:str, parents_name:str, equip_name:str, kids_name:str = ""):
    if kids_name:
        exrx_link = fitdb.pull_fix_and_return_link_using_names(musclegroup, parents_name, equip_name, kids_name)
        return(exrx_link)
    else:
        exrx_link = fitdb.pull_fix_and_return_link_using_names(musclegroup, parents_name, equip_name)
        return(exrx_link)



# OBVS WANT ONBOARDING TOO BUT THAT WOULD BE BEFORE OTHER STUFF,
# THIS IS LEGIT JUST FOR LOADING SOME IMAGES TO CACHE AND A BASIC TUTORIAL FOR FIRST TIME USERS BOSH!



# ---- START MAIN EXERCISE PAGE APP ----

def run():

    # ---- session state variable declarations ----

    if "images" not in st.session_state:
        st.session_state["images"] = {}

    # ---- page setup ----

    st.set_page_config(page_title="Onboarding", page_icon=":muscle:")

    files_list = find_image_files()

    st.write("##")

    current_session = st.session_state["session"]
    session_name = st.session_state['session_name']
    keys_list = list(current_session)
    muscle = keys_list[0] # for exercise 1
    muscle_justname = set_muscle_just_name(muscle)

    temp_equip = get_equip_list(muscle_justname)
    equip_list = []
    for equip in temp_equip:
        equip_list.append(equip[0])
    equip_tuple = tuple(equip_list)

    #equip_select = st.radio("Choose Equipment", equip_tuple)+
    #equip_select = st.selectbox(
    # 'Choose Equipment',equip_tuple)
     #parented_exercises = get_equipexercises_parent(equip_select)

    equip_select = st.multiselect(
     'Choose Equipment',
     equip_tuple,
     ['Barbell'])

    
    just_exercises_list = []
    exercise_equipment = get_equipexercises_basic(equip_select)
    for exercise in exercise_equipment:
        parent, child, equip = exercise[0], exercise[1], exercise[2]
        if child:
            just_exercises_list.append(f"{child} -> {parent} [{equip}]")

        else:
            just_exercises_list.append(f"{parent} [{equip}]")    
        
        
    current_equipex_name = st.selectbox("Choose An Exercise", just_exercises_list)

    st.write(current_equipex_name)

    exrx_exercise_link = split_current_equipex_name_for_link(current_equipex_name, muscle_justname)

    st.write(exrx_exercise_link)

    shortname_index = exrx_exercise_link.rfind("/")
    shortname = exrx_exercise_link[shortname_index+1:]
    
    ss_index = exrx_exercise_link.rfind("/")
    ssnamepath = f"images/{exrx_exercise_link[ss_index+1:]}.png" 

    st.write(shortname)

    for file in files_list:
        print(file)
        
        if current_equipex_name in st.session_state["images"]:
            print(f"{ssnamepath = }")
            st.subheader(ssnamepath)
            return(ssnamepath)

        if file == shortname:
            if shortname not in st.session_state["images"]:
                st.subheader(shortname)
                #st.session_state["images"][current_equipex_name] = "images\BBBenchPress.png" 


    # ONCE THIS, which is adding it to session states
    # THEN ADD THE FIRST LOADED IMG FOR EACH EQUIP SO ITS THERE
    # THEN ADD SOME MOST POP?
    # THEN CLEAN UP AND ADD BASE LAYOUT FOR TUT (could skip)

    # THEN ON TO ACTUAL EQUIPEX IMPLEMENTATION OoOOooOOoooooo


if __name__ == "__main__":
    run()