# main streamlit dashboard page
# imports 
# for web app and book format
import streamlit as st
# for data manipulation
import pandas as pd
# for timing - changing this if you want to other better time but if fine for now
from time import sleep
# for images
from PIL import Image
# integrations for db access, workout calculations 
import integration_database as fitdb
import integration_workout as wocalc
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
        st.image("https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Only-Muscle-Img-NOBG_SMALL-SHADOW-CENTERED-1-300x142.png")
    if mg == "Back":
        st.image("https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Targets-Synergists-LIGHTBG_SMALL-1-1-1-1-1-1-1-300x142.png")


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

    if equip_exercise_name in st.session_state["images"]:
        print(f"{ssnamepath}")
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

    # TRY IMPLEMENT LOADING BAR THING HERE OOO - again full idea is maybe to prompt beforehand and load some 
    # or have short load on first run/if doesnt find any cached images (its like a short setup basically)
    

    #split_current_equipex_name_for_link(current_equipex_name)
            
    
    with st.expander(f"Quick Preview -> {current_equipex_name}", True):
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
        st.image(img_path)

    st.write("##")

    has_chosen_equipmentexercise = st.button('CHOOSE THIS EXERCISE')

    st.write("##")


    # CONTAINER FOR EVERYTHING BEFORE SELECTING EQUIPMENT!
    # not considered changing equipment cases yet until this is working fine
    with st.container():

        if has_chosen_equipmentexercise:

            if info[2]:
                st.markdown(f"##### [ 1 ] - {muscle_justname} - ")
                st.write(f"Modifier : {info[2]}")
                get_image_for_muscle_group(muscle_justname)
                st.write("##")

            elif info[2] == None:
                st.markdown(f"##### [ 1 ] - {muscle_justname}")
                st.write("Modifier : Nope")
                get_image_for_muscle_group(muscle_justname)
                st.write("##")



            # need some basic validation for if actually has stats (since may not, and much more likely once equipment), would still like some dummy/cute data or even explainer in its place
            # ---- PREVIOUS SETS COMPARISON EXPANDER [ALPHA] ----
            with st.expander(f"Previous Stats For {muscle_justname}"):
                    

                previous_set = grab_previous_set_data(active_user, session_name, muscle_justname)
                amount_of_sets = len(previous_set)
                
                if previous_set:

                    if amount_of_sets == 3:

                        #BUG: IF USER HAS MORE THAN 3 SETS SAVED FOR EXERCISE THIS ERRORS (shouldnt be able to happen technically at this stage but in future will want so it is moderate oof)
                        #BUG: Note may have been unrelated error but still errored tbf so this is clearly a possible sticking point, need LBYL or EAFP

                        psetcol1, psetcol2, psetcol3, psetcol4 = st.columns(4)

                        set_1 = previous_set[0]
                        set_2 = previous_set[1]
                        set_3 = previous_set[2]

                        set_1_reps, set_1_weight, set_1_total_weight = set_1[1], set_1[2], set_1[3]
                        set_2_reps, set_2_weight, set_2_total_weight = set_2[1], set_2[2], set_2[3]
                        set_3_reps, set_3_weight, set_3_total_weight = set_3[1], set_3[2], set_3[3]

                        set_1_weight = float(set_1_weight)
                        set_1_total_weight = float(set_1_total_weight)

                        set_2_weight = float(set_2_weight)
                        set_2_total_weight = float(set_2_total_weight)

                        set_3_weight = float(set_3_weight)
                        set_3_total_weight = float(set_3_total_weight)

                    with psetcol4:
                        want_prev_weight = st.checkbox('Previous Weight', True)
                        want_prev_reps = st.checkbox('Previous Reps', False)
                        if st.session_state["currentset"] > 1:
                            want_prev_totweight = st.checkbox('Prev Total Weight', False)     

                #FIXME: Errors here if it doesn't find the pre-existing data, should be an easy enough fix tbf
                # should note to user that increase weight is always best more clearly
                # possibly a toggle for show weight reps or total weight in col4? - defo test this tbf
                
                    with psetcol1:
                        st.write("##### Set 1")
                        set1_reps_delta = st.session_state["exset1reps"] - set_1_reps
                        set1_weight_delta = st.session_state["exset1"] - set_1_weight
                        # exsetX stores the weight, defaults to false hence why use greater than 1 (i.e. any weight and not false turns it on)
                        if st.session_state["exset1"] > 1:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_1_weight} KG", delta=f"{set1_weight_delta} KG today")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_1_reps} reps", delta=f"{set1_reps_delta} reps today")
                        else:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_1_weight} KG")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_1_reps} reps")

                        if st.session_state["currentset"] > 1:
                            if want_prev_totweight:
                                set1_current_session_tot_weight = st.session_state["exset1"] * st.session_state["exset1reps"]
                                set1_tot_weight_delta = set1_current_session_tot_weight - set_1_total_weight
                                st.metric(label="Previ Total Weight", value=f"{set_1_total_weight} reps", delta=f"{set1_tot_weight_delta} kg lifted today")

                    with psetcol2:
                        st.write("##### Set 2")
                        set2_reps_delta = st.session_state["exset2reps"] - set_2_reps
                        set2_weight_delta = st.session_state["exset2"] - set_2_weight

                        if st.session_state["exset2"] > 1:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_2_weight} KG", delta=f"{set2_weight_delta} KG today")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_2_reps} reps", delta=f"{set2_reps_delta} reps today")
                        else:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_2_weight} KG")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_2_reps} reps")

                        if st.session_state["currentset"] > 2:
                            if want_prev_totweight:
                                set2_current_session_tot_weight = st.session_state["exset2"] * st.session_state["exset2reps"]
                                set2_tot_weight_delta = set2_current_session_tot_weight - set_2_total_weight
                                st.metric(label="Previ Total Weight", value=f"{set_2_total_weight} reps", delta=f"{set2_tot_weight_delta} kg lifted today")

                    with psetcol3:
                        st.write("##### Set 3")
                        set3_reps_delta = st.session_state["exset3reps"] - set_3_reps
                        set3_weight_delta = st.session_state["exset3"] - set_3_weight

                        if st.session_state["exset3"] > 1:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_3_weight} KG", delta=f"{set3_weight_delta} KG today")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_3_reps} reps", delta=f"{set3_reps_delta} reps today")
                        else:
                            if want_prev_weight:
                                st.metric(label="Previous Weight", value=f"{set_3_weight} KG")
                            if want_prev_reps:
                                st.metric(label="Previous Reps", value=f"{set_3_reps} reps")

                        if st.session_state["currentset"] > 3:
                            if want_prev_totweight:
                                set3_current_session_tot_weight = st.session_state["exset3"] * st.session_state["exset3reps"]
                                set3_tot_weight_delta = set3_current_session_tot_weight - set_3_total_weight
                                st.metric(label="Prev Total Weight", value=f"{set_3_total_weight} reps", delta=f"{set3_tot_weight_delta} kg lifted today")    
                
                else:
                    st.write("##### No Previous Set Info")


            # ---- CURRENT SETS TRACKER EXPANDER ----
            with st.expander("Sets For Exercise", True):
                setcol1, setcol2, setcol3, setcol4 = st.columns(4)
                
                if (st.session_state["currentset"]) < 4:
                    setcol4.write("Current Set")
                    setcol4.write(st.session_state["currentset"])
                else:
                    setcol4.markdown("""### COMPLETE """)
                
                if st.session_state["exset1reps"] < 1:
                    setcol1.write(":x:")
                elif st.session_state["exset1reps"] > 1:
                    set1_reps = st.session_state["exset1reps"]
                    setcol1.write(f"{set1_reps} reps :white_check_mark:")
                else:
                    setcol1.write(":white_check_mark:")

                if st.session_state["exset2reps"] < 1:
                    setcol2.write(":x:")
                elif st.session_state["exset2reps"] > 1:
                    set2_reps = st.session_state["exset2reps"]
                    setcol2.write(f"{set2_reps} reps :white_check_mark:")
                else:
                    setcol2.write(":white_check_mark:")

                if st.session_state["exset3reps"] < 1:
                    setcol3.write(":x:")
                elif st.session_state["exset3reps"] > 1:
                    set3_reps = st.session_state["exset3reps"]
                    setcol3.write(f"{set3_reps} reps :white_check_mark:")
                else:
                    setcol3.write(":white_check_mark:")


            # ---- EXERCISE LOGGGER FORM ----
            ## if 4th set hide form, else show 
            if (st.session_state["currentset"]) < 4:
                with st.form(key=f"exercise_logger_1"):

                    logcol1, logcol2, logcol3 = st.columns([3,2,1])

                    # SETS DICKHEAD - OR DOES IT GO FOR EVERY SET????

                    with logcol1:
                        the_reps = st.number_input("Enter Reps Completed", step=1, key="the_reps")

                    with logcol2:
                        # obvs make a toggle for changing weight units - has considerations obvs 
                        the_weight = st.number_input("Enter Weight Used In KG", 5.0, 500.0, step=0.5, key="the_weight")

                    
                    with logcol3:
                        st.write("Start Timer")
                        # logic here for what set!
                        #submit_exercise_log = st.form_submit_button(label="Set Done", on_click=update_db, args=[(active_user, "001", session_name, f"1.{muscle_justname}", current_set, the_reps, the_weight, the_reps*the_weight, exercise_rest_time)])
                        submit_exercise_log = st.form_submit_button(label="Set Done")


                    # ---- SUBMIT EXERCISE FORM LOGIC ----
                    if submit_exercise_log:

                        update_db((active_user, "001", session_name, f"1.{muscle_justname}", current_set, the_reps, the_weight, the_reps*the_weight, exercise_rest_time))

                        coltime, colres = st.columns([2,2])
                        with colres:
                            with st.expander("Results"):
                                weight_lifted = [the_reps*the_weight]
                                if current_set == 1:
                                    st.session_state["exset1reps"] = the_reps
                                    df = pd.DataFrame({"set1":weight_lifted})
                                elif current_set == 2:
                                    st.session_state["exset2reps"] = the_reps
                                    set1totweight = st.session_state["exset1reps"] * st.session_state["exset1"]
                                    df = pd.DataFrame({"set1":set1totweight,"set2":weight_lifted})
                                elif current_set == 3:
                                    st.session_state["exset3reps"] = the_reps
                                    set1totweight = st.session_state["exset1reps"] * st.session_state["exset1"]
                                    set2totweight = st.session_state["exset2reps"] * st.session_state["exset2"]
                                    df = pd.DataFrame({"set1":set1totweight,"set2":set2totweight,"set3":weight_lifted})
                                st.dataframe(df.T)
                        with coltime:
                            with st.expander("Timer", True):
                                if submit_exercise_log:
                                    did_timer_finish = print_timer(exercise_rest_time)
                                    if did_timer_finish:
                                        st.write(did_timer_finish)
                                        #st.session_state["exset1"] = True
                                        st.experimental_rerun()


            if (st.session_state["currentset"]) >= 4:
                st.write("##")
                # BUTTON FOR NEXT EXERCISE & SOME STATS N SHIT (& share but not rn) maybe nice to have next name too but text
                # should legit just go, could pass args if needed but shouldnt really need to tbf?
                # looks ugly af rn but meh can improve in future is just to show basic flow/logic/idea for personal project mvp
                with st.container():
                    _,_,tendcol1,tendcol2 = st.columns(4)
                    tendcol1.write('#### NEXT UP >>')
                    tendcol1.write('exercise name')
                    tendcol2.button('GO TO EXERCISE 2')

                with st.container():
                    endcol1,endcol2 = st.columns([2,1])
                    
                    st.write("You lifted blah")
                    set1totweight = st.session_state["exset1reps"] * st.session_state["exset1"]
                    set2totweight = st.session_state["exset2reps"] * st.session_state["exset2"]
                    set3totweight = st.session_state["exset3reps"] * st.session_state["exset3"]
                    final_ex1_totweight = set1totweight + set2totweight + set3totweight

                    # NEED FIX DELTA, AND OBVS NEEDS CHECK FOR IF DATA EXISTS FIRST - LEGIT JUST USE DB QUERIES MORE
                    # - START TRACKING IN DETAIL EVERY SINGLE VAR YOU NEED!

                    st.metric(label="Ex1 Weight Lifted", value=f"{final_ex1_totweight} KG", delta=f"{0} kg from last session")    
                    
                    compare_weight_tuple = get_weight_comparision(final_ex1_totweight)
                    st.write(compare_weight_tuple)

                    st.write("##")
                    # obvs needs timestamp, want logic for if ur not consistent too as its important (e.g. 4 weeks off shouldnt validate a change!)
                    st.write("Weeks on Exercise = X, We Recommend You Do For X More (consistently)")
                    
                    endcol2.success("NEW PB - LEGOOOOO!")




        def show_running_info():
            """ for the current session """
            # maybe have as a general function, not as a streamlit specific, and it just returns what is needed for the streamlit sections like metric or whatever
            st.write("Make Me A Metric")




if __name__ == "__main__":
    run()