# main streamlit dashboard page
# imports 
# for web app
import streamlit as st
# for data manipulation
import pandas as pd
# for images
from PIL import Image
# for timing - changing this if you want to other better time but if fine for now
import time


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
        time.sleep(1)
        if secs == 1:
            reached_end = True
    if reached_end == True:
        return("COMPLETE")
    else:
        return("UNFINISHED")

def convert_seconds_to_minutes(seconds) -> int:
    secs = (seconds % 60)
    return(f"{(seconds // 60)} min {secs} secs")

def set_muscle_just_name(muscle:str) -> str:
    if muscle == "Front":
        muscle_just_name = "Front Delt"
    else:
        muscle_just_name = muscle
    return(muscle_just_name)


# ---- for ordering containers ----
topper = st.container()
exercise_section = st.container()
amount_of_sets_section = st.container()
timer_info = st.container()
sets_container = st.container()
exercise_expander = st.container()
timer_expander = st.expander("Timer", True)

#timer = st.container()

if "set1" not in st.session_state:
    st.session_state["set"] = 0

if "set" not in st.session_state:
    st.session_state["set"] = 0

def run():
    # TOPPER container
    with st.container():
        with topper:
            st.subheader(f":muscle: {st.session_state['session_name']}")
            current_session = st.session_state["session"]
            st.write("##")

        # BE SICK TO HAVE LIKE A THING IF U DO IT MANUALLY THAT SAYS HOW APPROPRIATE IT IS FOR THE CURRENT MG N EQUIP
        # OBVS GUNA HAVE DYNAMIC RECOMMENDATION - ALSO PRESETS THE VALUE! - BASED ON MG N EQUIP (n level? n else?)

        amount_of_exercises = len(current_session)
        options_range = range(1,amount_of_exercises+1)

        st.write("##")

        with exercise_section:
            with st.expander("Exercise Selector", True):
                exercise = st.select_slider(
                    'Select Exercise Number',
                    options=options_range)
                st.write('Current Exercise Is', exercise)

        with amount_of_sets_section:
            with st.expander("Set Selector", True):
                sets_count = st.slider("Select How Many Sets",1,5,3,1)
        
        with timer_info:
            with st.expander("Timer Selector"):
                st.write("Note Timer will be set dynamically for you, but you can change it if you wish")
                number = st.slider('Set The Timer', 15, 300, 60, 5)
                st.write("Current Timer :", number, "sec")
                in_mins = convert_seconds_to_minutes(number)
                st.write(f"Or {in_mins}") 

            st.write("##")

            # COULD LITERALLY DO THIS AS ONCLICK
            # ON CLICK BUTTON
            # RUN THIS AS A FUNCTION, PASSING IN THE NEXT EX NUMBER AS AN INT OR EVEN LIKE SLIDER POSITION THAT CANT BE CHANGED WHATEVER
            # WORTH FIGURING OUT NOW THO? hmmmm

            exercises_in_session = len(current_session)
            st.write(f'Current Exercise {exercise} Of {exercises_in_session}')
            i = exercise

            #print(f"{current_session = }")

            keys_list = list(current_session)
            muscle = keys_list[i-1]
            muscle_justname = set_muscle_just_name(muscle)
            info = current_session[muscle]

            # print(f"{muscle = }")
            # print(f"{info = }")

            # note containters maybe even one for exercises, equipment etc lawd

            if info[2]:
                st.markdown(f"##### [ {i} ] - {muscle_justname} - ")
                st.write(f"Modifier : {info[2]}")
                get_image_for_muscle_group(muscle_justname)
                st.write("##")

            if info[2] == None:
                st.markdown(f"##### [ {i} ] - {muscle_justname}")
                st.write("Modifier : Nope")
                get_image_for_muscle_group(muscle_justname)
                st.write("##")
    
            
            sets = st.session_state["set"]
            #sets = int(sets_count) ## FIGURE OUT HOW THIS WILL WORK FFS - ALSO CONSIDER NOW PAGES AND MAYBE JUST DO WITH THAT AS CONTROL FLOW?
            
            def set_calculator():
                # session state or sumnt for sets idk?
                ##############################################################################
                # SAVE THE SHIT TO THE DB - COULD LEGIT QUERY THE DB FOR LOTS OF LOGIC TBF!! #
                ##############################################################################

                # LEGIT JUST USE DB OR BOOK &OR PAGE PARAMS!
                # https://docs.streamlit.io/library/api-reference/utilities/st.experimental_get_query_params
                # https://docs.streamlit.io/library/api-reference/utilities/st.experimental_set_query_params
                pass

                # then basically once full (list is of length sets) wipe it, and set it to a st.sessionstate (so cant redo the ex)
                # and save the shit to the db

            with sets_container:
                with st.expander("Sets For Exercise"):
                    setcol1, setcol2, setcol3 = st.columns(3)
                    sets = st.session_state["set"]
                    st.write(f"Current Set = {sets} of {sets_count}")
                    page_params = (st.experimental_get_query_params())
                    st.write(page_params)
                    if sets == 1:
                        setcol1.write("SET 1")
                        st.session_state["set1"] = page_params
                    elif sets == 2:
                        setcol2.write("SET 2")
                    elif sets == 3:
                        setcol3.write("SET 3")

            with st.form(key=f"exercise_logger_{i}"):
                logcol1, logcol2, logcol3 = st.columns([3,2,1])

                # SETS DICKHEAD - OR DOES IT GO FOR EVERY SET????

                with logcol1:
                    reps = st.number_input("Enter Reps Completed", step = 1)

                with logcol2:
                    # obvs make a toggle for changing weight units - has considerations obvs 
                    weight = st.number_input("Enter Weight Used In KG", 5, 500)

                with logcol3:
                    st.write("Start Timer")
                    submit_exercise_log = st.form_submit_button(label="Set Done")

                if submit_exercise_log:
                    with exercise_expander:
                        with st.expander("Results"):
                            weight_lifted = [reps*weight]
                            df = pd.DataFrame({"weight_lifted":weight_lifted})
                            st.dataframe(df.T)

                    coltime, _ = st.columns([2,1])
                    with coltime:
                        with timer_expander:
                            if submit_exercise_log:
                                did_timer_finish = print_timer(number)
                                if did_timer_finish:
                                    print(did_timer_finish)
                                    st.write(did_timer_finish)
                                    st.experimental_set_query_params(
                                        set_numb=st.session_state["set"],
                                        selected=[weight_lifted],
                                    )
                                    st.session_state["set"] += 1
                                    st.experimental_rerun()



                                    



        # st.checkbox('Next Exercise?', key=f"NextEx{i}")

            # JUST CONTINUE NOW THO PLS NEED ACTUAL LOG FOR EXAMPLE - AND WILL NEED SOME LIGHT DB SETUP

            # TBF JUST WANT SOMETHING THAT DOESN'T GIVE CONTROL FLOW UP TO PRINT NEXT [i] UNTIL CHECK BOX OR WHATEVER
            # MEANS COULD THEN EVEN PUT TIMER HERE TOO... 

            # OK SO THINGS TO ADD
                # - logging reps, weight (and time but *you* dont log it, its just saved)
                # - recommending time [1 - RELATED weak]
                # - recommending equipment [1 - RELATED]
                # - recommending exercise [1 - RELATED]
                # - running stats
                # - previous stats
                # - then future reps checker based on previous stats (tbf can be current too, just any time at ceil/floor)

        # DONT FORGET ON CHANGE AND ON CLICK - SURELY COULD HELP https://docs.streamlit.io/library/api-reference/session-state#use-callbacks-to-update-session-state

        #st.write(current_session)

        # FOR REFERENCE
    with st.container():
        
        st.write("##")
        st.write("##")
        st.write("##")

        # ---- for st.metric header widget ----
        col1, col2, col3, col4 = st.columns(4)

        # note delta can be can be off, normal, or inverse
        col1.metric(label="Total Weight Lifted", value=f"${100:.2f}", delta=f"{10:.2f}", delta_color="normal")
        col2.metric(label="Upper Weight Lifted", value=f"${200:.2f}", delta=f"{20:.2f}", delta_color="normal")
        col3.metric(label="Lower Weight Lifted", value=300, delta=0, delta_color="off") 
        col4.metric(label="Exercises Complete", value=400, delta=0, delta_color="off")

        st.write("---")


if __name__ == "__main__":
    run()


# https://blog.streamlit.io/how-to-create-interactive-books-with-streamlit-and-streamlit-book-in-5-steps/

#chest = "https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Targets-Synergists-LIGHTBG_SMALL-1-1-1-1-1-1-1-300x142.png"
#chest2 = 'https://thehardgainerbible.com/wp-content/uploads/2022/03/Chest-Main-Only-Muscle-Img-NOBG_SMALL-SHADOW-CENTERED-1-300x142.png'

#number = st.number_input('Insert Seconds', min_value=30, step=1)
#st.write(f'The current timer is {number:.0f}', )

#while st.checkbox('Next Exercise?', key=f"NextEx{i}") == False:
    #timee.sleep(1)