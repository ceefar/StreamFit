# exercise one page
# imports 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc
# for data manipulation
import pandas as pd
# for timing - changing this if you want to other better time but if fine for now
from time import sleep
# for file manipulation and folder navigation 
import os
# integrations for db access, workout calculations 
import integration_database as fitdb
import integration_workout as wocalc
import integration_scrape_exrx as exrx
import screenshotter as sss #selenium screenshotter

# ---- functions ----

# if this works and am using this format (for v0.2 / MVP anyways) then put the below functions in their own module

def set_muscle_just_name(muscle:str) -> str:
    if muscle == "Front":
        muscle_just_name = "Front Delt"
    else:
        muscle_just_name = muscle
    return(muscle_just_name)


def get_image_for_muscle_group(mg):
    if mg == "Chest":
        return("https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Only-Muscle-Img-NOBG_SMALL-SHADOW-CENTERED-1-300x142.png")
    if mg == "Back":
        return("https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Targets-Synergists-LIGHTBG_SMALL-1-1-1-1-1-1-1-300x142.png")


def print_timer(max_time:int = 60):
    """ defaults to 60 seconds """
    ph = st.empty()
    N = max_time
    reached_end = False
    for secs in range(N,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
        sleep(1)
        if secs == 0:
            reached_end = True
    if reached_end == True:
        return("COMPLETE")
    else:
        return("UNFINISHED")


def convert_seconds_to_minutes(seconds) -> int:
    secs = (seconds % 60)
    return(f"{(seconds // 60)} min {secs} secs")


@st.cache
def get_equip_list(muscle):
    exequip = fitdb.get_all_equip_for_mg(muscle)
    return(exequip)


@st.cache
def update_db(args):
    for i, arg in enumerate(args):
        #print(f"{arg = }")
        if i == 0:
            name_of_active_user = arg
        if i == 1:
            user_id = arg
        if i == 2:
            name_of_session = arg
        if i == 3:
            name_of_mgnumb = arg
        if i == 4:
            the_current_set = arg
            st.session_state["currentset"] += 1
        if i == 5:
            completed_reps = arg
        if i == 6:
            if st.session_state["currentset"] == 2:
                st.session_state["exset1"] = arg
            if st.session_state["currentset"] == 3:
                st.session_state["exset2"] = arg
            if st.session_state["currentset"] == 4:
                st.session_state["exset3"] = arg
            used_weight = arg
        if i == 7:
            the_total_weight = arg
        if i == 8:
            the_rest_time = arg

    sessionID = st.session_state[f"{name_of_active_user}_sessionID"]
    fitdb.add_exercise_set_data_to_db(name_of_active_user, sessionID, name_of_session, name_of_mgnumb, the_current_set, completed_reps, used_weight, the_total_weight, the_rest_time)


@st.cache
def grab_previous_set_data(userName, sessionName, muscleNumb) -> tuple:
    """ pls write me ceefar """
    # obvs this will be equip so dw too much about weird way of doing this,
    # for ex 2 just do same since we know which exercise number it is
    needed_mg_name_format = f"1.{muscleNumb}" 
    previous_set = fitdb.find_previous_sets_for_muscle(userName, sessionName, needed_mg_name_format)
    return(previous_set)


@st.cache
def section_previous_set_data(previous_set:tuple) -> tuple:
    """ properly sections and reformats previous set data """
    # maybe im overthinking but implementing now for idea that are multiple sets, like sure can do for 3 sets everytime easy but what happens if 2 sets, 
    # what happens if user ended early, what happens for 4 in future, what happens if corrupted data etc
    # actually not guna use yet but just left basic logic, mostly as yeah im still unsure about its proper implementation so moving on for now
    amount_of_sets = len(previous_set)
    if amount_of_sets == 3:
        set_1 = previous_set[0]
        set_2 = previous_set[1]
        set_3 = previous_set[2]
    

@st.cache
def get_rest_time_from_muscle(mg:str, split:str) -> int:
    rest_time = wocalc.calculate_rest_time_v0(mg, split)
    print(f"{rest_time = }")
    return(rest_time)


@st.cache
def get_weight_comparision(weight:int) -> tuple[str,float,str]:
    compare_tuple = wocalc.get_real_world_weight_comparison(weight)
    print(f"{compare_tuple = }")
    return(compare_tuple)


@st.cache
def get_equipexercises_parent(equip):
    childparentequipexercises = fitdb.get_equipexercises_with_childparent(equip)
    return(childparentequipexercises)


def get_equipexercises_basic(equiplist):
    return(fitdb.get_equipexercises_forlist_basic(equiplist))



def get_ss(equip_exercise_name:str, muscle_justname:str):
    # what you wanna do here is pass the name or path or link or whatever (the path tbf)
    # and save it in a session state called "images", so if path is in ss[images] then it can just use it, else it finds it!
    # have finds link function in here since just makes more sense for flow of session state (i think anyways)
    
    exrx_exercise_link = split_current_equipex_name_for_link(equip_exercise_name, muscle_justname)

    ss_index = exrx_exercise_link.rfind("/")
    ssnamepath = f"images/{exrx_exercise_link[ss_index+1:]}.png" 




    # NOTE - MAKE OWN FUNCTION PLS
    # NEW - FOR CHECKING IF IN IMAGES FOLDER - MAKE OWN FUNCTION THO?!!?!!!

    temp_pngname = f"{exrx_exercise_link[ss_index+1:]}.png"
    print(f"{temp_pngname = }")

    files_and_directories = os.listdir("images")
    print(f"{files_and_directories = }")

    if temp_pngname in files_and_directories:
        print("JUST LOAD FROM DIRECTORY DUH!")
        print(f"{ssnamepath = }")
        return(ssnamepath)
        # note to do that you just return the ssnamepath var like below bosh (nothing else needed as return will kill control flow there bosh bosh)

    # also note sometimes may want to turn this off for testing, well until can do a generalised load or sumnt idk yet how would work in final version tbf

    # END NEW ADDITION



    if equip_exercise_name in st.session_state["images"]:
        print(f"{ssnamepath = }")
        return(ssnamepath)
    else:
        with st.spinner('Grabbing Exercise Data...'):
        
            # if not in session state (hasn't been screenshotted before and saved to images cache (or just already in images cache))
            # add it to the images cache dictionary {key->name:value->path}
            st.session_state["images"][equip_exercise_name] = "images\BBBenchPress.png" 
            # take the screenshot, should probably flip the order here incase screenshot errors
            path_to_ss = sss.take_selenium_screenshot(exrx_exercise_link) # needs url to do this properly
        st.success('Done & Saved To Cache!')
    return(path_to_ss)


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


def create_icon(font_size:int = "", font_color:str = ""):
    """ testing -> returns the string needs with format var section to input the icon you want, format order is important based on parameters """

    # call like this
    # stc.html(create_icon().format("cloud"),height=50)

    if font_size and font_color:
        icon_create = """ <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"><i class="material-icons" style="font-size:{}rem; color:{};>{}</i> """
    elif font_size:
        icon_create = """ <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"><i class="material-icons" style="font-size:{}rem;>{}</i> """
    elif font_color:
        icon_create = """ <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"><i class="material-icons" style="color:{};>{}</i> """
    else:
        icon_create = """ <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"><i class="material-icons">{}</i> """
    return(icon_create)


# ---- v2 ----


@st.cache
def update_db_v2(args):
    for i, arg in enumerate(args):
        #print(f"{arg = }")
        if i == 0:
            name_of_active_user = arg
        if i == 1:
            user_id = arg
        if i == 2:
            name_of_session = arg
        if i == 3:
            name_of_mgnumb = arg
        if i == 4:
            the_current_set = arg
            st.session_state["currentset"] += 1
        if i == 5:
            completed_reps = arg
        if i == 6:
            if st.session_state["currentset"] == 2:
                st.session_state["exset1"] = arg
            if st.session_state["currentset"] == 3:
                st.session_state["exset2"] = arg
            if st.session_state["currentset"] == 4:
                st.session_state["exset3"] = arg
            used_weight = arg
        if i == 7:
            the_total_weight = arg
        if i == 8:
            the_rest_time = arg
        if i == 9:
            equipex = arg

    sessionID = st.session_state[f"{name_of_active_user}_sessionID"]
    fitdb.add_exercise_set_data_to_db_v2(name_of_active_user, sessionID, name_of_session, name_of_mgnumb, equipex, the_current_set, completed_reps, used_weight, the_total_weight, the_rest_time)


def split_current_equipex_shortname(equipex_name:str, muscle_justname:str) -> str:
    """ self referencing, returns link, should find an easier way to do this tho """
    # if is a child
    if "->" in equipex_name:
        kids_index = equipex_name.find("->")
        equip_index = equipex_name.find("[")
        kids_name = equipex_name[kids_index+3:equip_index-1]
        parents_name = equipex_name[:kids_index]
        equip_name = equipex_name[equip_index+1:-1]
        parents_name = parents_name.strip()
        shortname = use_name_get_shortname(muscle_justname, parents_name, equip_name, kids_name)
        return(shortname)
    else:
        # if its a parent (no child)
        equip_index = equipex_name.find("[")
        equip_name = equipex_name[equip_index+1:-1]
        parents_name = equipex_name[:equip_index]
        parents_name = parents_name.strip()
        # st.write(f"{parents_name = }")
        # st.write(f"{equip_name = }")
        shortname = use_name_get_shortname(muscle_justname, parents_name, equip_name)
        return(shortname)


def use_name_get_shortname(musclegroup:str, parents_name:str, equip_name:str, kids_name:str = ""):
    if kids_name:
        shortname = fitdb.get_exercise_shortname(musclegroup, parents_name, equip_name, kids_name)
        return(shortname)
    else:
        shortname = fitdb.get_exercise_shortname(musclegroup, parents_name, equip_name)
        return(shortname)


@st.cache
def grab_previous_set_data_v2(userName, sessionName, muscleNumb, equipExercise) -> tuple:
    """ pls write me ceefar """
    # obvs this will be equip so dw too much about weird way of doing this,
    # for ex 2 just do same since we know which exercise number it is
    needed_mg_name_format = f"1.{muscleNumb}" 
    previous_set = fitdb.find_previous_sets_for_muscle_v2(userName, sessionName, needed_mg_name_format, equipExercise)
    return(previous_set)



# ---- START MAIN EXERCISE PAGE APP ----

def run():

    # ---- page setup ----

    st.set_page_config(page_title="Exercise", page_icon=":muscle:")

    # ---- session state variable declarations ----

    if "exset1" not in st.session_state: # CURRENTLY STORES WEIGHT AS A SESSIONSTATE VARIABLE BTW
        st.session_state["exset1"] = False

    if "exset1reps" not in st.session_state:
        st.session_state["exset1reps"] = 0

    if "exset2" not in st.session_state: # CURRENTLY STORES WEIGHT AS A SESSIONSTATE VARIABLE BTW
        st.session_state["exset2"] = False

    if "exset2reps" not in st.session_state:
        st.session_state["exset2reps"] = 0

    if "exset3" not in st.session_state: # CURRENTLY STORES WEIGHT AS A SESSIONSTATE VARIABLE BTW
        st.session_state["exset3"] = False

    if "exset3reps" not in st.session_state:
        st.session_state["exset3reps"] = 0

    if "currentset" not in st.session_state:
        st.session_state["currentset"] = 1

    if "images" not in st.session_state:
        st.session_state["images"] = {}

    if "exercise1" not in st.session_state:  # stores the current exercise 1 name for validation between exercise 1 select and exercise 1 start
        st.session_state["exercise1"] = ""


    # EXPERIMENTAL / TESTING -> for select vs start, seeing best way to pass the vars between pages and not force reruns
    if "ex1_img_path" not in st.session_state:
        st.session_state["ex1_img_path"] = ""

    if "ex1_current_equipex_name" not in st.session_state:
        st.session_state["ex1_current_equipex_name"] =""

    if "ex1_shortname" not in st.session_state:
        st.session_state["ex1_shortname"] = ""
    # END TESTING


    # ---- variable declarations ----

    current_session = st.session_state["session"]
    session_name = st.session_state['session_name']
    keys_list = list(current_session)
    muscle = keys_list[0] # for exercise 1
    muscle_justname = set_muscle_just_name(muscle)
    info = current_session[muscle]
    amount_of_exercises = len(current_session)
    options_range = range(1,amount_of_exercises+1) # SHOULD USE TO SHOW 1 of X remaining duh!
    active_user = st.session_state["active_user"]
    current_set = st.session_state["currentset"]
    # need function for this (and others tbf) to be dynamic but for now just static
    exercise_rest_time = get_rest_time_from_muscle(muscle_justname, session_name)

    #print(f"{info = }")
    #print(f"{muscle_justname = }")
    #print(f"{muscle = }")
    #print(f"{session_name = }")
    #print(f"{current_session = }") 

    # ---- PAGE START ----

    # note has to be almost one of the first things you do right, so just get a basic for now on new branch anyway so chill

    st.title(f"Exericse 1 : {muscle_justname}")
    st.subheader(f":muscle: {session_name}")

    st.write("##")

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

    st.write("##")

    # TRY IMPLEMENT LOADING BAR THING HERE OOO - again full idea is maybe to prompt beforehand and load some 
    # or have short load on first run/if doesnt find any cached images (its like a short setup basically)
    

    #split_current_equipex_name_for_link(current_equipex_name)
            
    
    with st.expander(f"Quick Preview", True):
        # FIXME :
        # obvs the above session state thing, also need new function for getting link from name (will have to format the link too)
        # clarify to user app faster once more images loaded, maybe through a success box or similar (alert if they have)
        # also maybe not an expander (idk tho) as nice to have a way to just run that code when its needed, not at start (would cache do that?)
        # also also make a funct to say do the most popular ones and defo the ones that it will start on for each loading page
        # and have them preload at the start of the app
        # obvs also ig have sumnt to pull image file names listed in that folder (or just a manually made list for now)
        # then just dont run the funct and instead send the image path if in that list
        # obvs could legit make a funct that goes through all links and saves them for me too / the user
        # to save time, do that and make it optional but dont use all images throughout as want to see any errors or potential sticking points
        img_path = get_ss(current_equipex_name, muscle_justname)
        _,midcol,_ = st.columns([1,3,1])
        midcol.markdown(f"""<h3 style="text-align:center">{current_equipex_name}</h3>""", unsafe_allow_html=True) 
        midcol.image(img_path)

    st.write("##")

    _,midcol2,_ = st.columns([2,3,1])
    has_chosen_equipmentexercise = midcol2.button('CHOOSE THIS EXERCISE')

    st.write("##")


    exrx_exercise_link = split_current_equipex_name_for_link(current_equipex_name, muscle_justname)
    shortname = split_current_equipex_shortname(current_equipex_name, muscle_justname)

    # obvs move to proper function place above page stuff
    exercise_info_list = exrx.grab_basic_exercise_info_from_exrx(exrx_exercise_link)

    
    if has_chosen_equipmentexercise:

        st.session_state["ex1_img_path"] = img_path
        st.session_state["ex1_current_equipex_name"] = current_equipex_name
        st.session_state["ex1_shortname"] = shortname

        st.write("##")
        midcol2.subheader("Start Exercise 1")
        
        # and remove the button?!! / else on screen?!?!!

        # NEW - TESTING - FILE MANIPULATION

   




if __name__ == "__main__":
    run()