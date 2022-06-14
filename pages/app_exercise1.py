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
# for db access
import integration_database as fitdb


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
    
    fitdb.add_exercise_set_data_to_db(name_of_active_user, name_of_session, name_of_mgnumb, the_current_set, completed_reps, used_weight, the_total_weight, the_rest_time)


def run():

    # page setup
    st.set_page_config(page_title="Exercise", page_icon=":muscle:")

    # ---- variable declarations ----

    if "exset1" not in st.session_state:
        st.session_state["exset1"] = False

    if "exset1reps" not in st.session_state:
        st.session_state["exset1reps"] = 0

    if "exset2" not in st.session_state:
        st.session_state["exset2"] = False

    if "exset2reps" not in st.session_state:
        st.session_state["exset2reps"] = 0

    if "exset3" not in st.session_state:
        st.session_state["exset3"] = False

    if "exset3reps" not in st.session_state:
        st.session_state["exset3reps"] = 0

    if "currentset" not in st.session_state:
        st.session_state["currentset"] = 1

    current_session = st.session_state["session"]
    session_name = st.session_state['session_name']
    keys_list = list(current_session)
    muscle = keys_list[0] # for exercise 1
    muscle_justname = set_muscle_just_name(muscle)
    info = current_session[muscle]
    amount_of_exercises = len(current_session)
    options_range = range(1,amount_of_exercises+1)
    active_user = st.session_state["active_user"]
    current_set = st.session_state["currentset"]
    # need function for this (and others tbf) to be dynamic but for now just static
    exercise_rest_time = 15

    st.title(f"Exericse 1 : {muscle_justname}")
    st.subheader(f":muscle: {session_name}")


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


    with st.expander("Sets For Exercise", True):
        setcol1, setcol2, setcol3, setcol4 = st.columns(4)
        
        setcol4.write("Current Set")
        setcol4.write(st.session_state["currentset"])
        
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


    with st.form(key=f"exercise_logger_1"):

        logcol1, logcol2, logcol3 = st.columns([3,2,1])

        # SETS DICKHEAD - OR DOES IT GO FOR EVERY SET????

        with logcol1:
            the_reps = st.number_input("Enter Reps Completed", step=1, key="the_reps")
            print(the_reps)

        with logcol2:
            # obvs make a toggle for changing weight units - has considerations obvs 
            the_weight = st.number_input("Enter Weight Used In KG", 5.0, 500.0, step=0.5, key="the_weight")

        with logcol3:
            st.write("Start Timer")
            # logic here for what set!
            #submit_exercise_log = st.form_submit_button(label="Set Done", on_click=update_db, args=[(active_user, "001", session_name, f"1.{muscle_justname}", current_set, the_reps, the_weight, the_reps*the_weight, exercise_rest_time)])
            submit_exercise_log = st.form_submit_button(label="Set Done")

        if submit_exercise_log:

            update_db((active_user, "001", session_name, f"1.{muscle_justname}", current_set, the_reps, the_weight, the_reps*the_weight, exercise_rest_time))


            # TRY JUST PRINT WITHOUT THE DF SEE IF IT LOOKS CLEANER


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
                            print(did_timer_finish)
                            st.write(did_timer_finish)
                            #st.session_state["exset1"] = True
                            st.experimental_rerun()





if __name__ == "__main__":
    run()