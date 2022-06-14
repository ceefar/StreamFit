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
    for secs in range(N,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

def convert_seconds_to_minutes(seconds) -> int:
    secs = (seconds % 60)
    return(f"{(seconds // 60)} min {secs} secs")


# ---- for ordering containers ----
topper = st.container()
exercise_section = st.container()
timer_info = st.container()
exercise_expander = st.container()
timer_expander = st.expander("Timer", True)

#timer = st.container()


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

            for i, (muscle, info) in enumerate(current_session.items()):
            
            # DO YOU EVEN NEED A FOR LOOP HERE (i mean defo no - but then how for i?)
            # PROBABLY CAN GET AWAY WITH COLS NOW BTW!
            # and maybe even 2 containters for top and then bottom (timer, info) - shit maybe even one for exercises, equipment etc lawd

                if exercise-1 == i:
                    if info[2]:
                        st.markdown(f"##### [ {i+1} ] - {muscle} - ")
                        st.write(f"Modifier : {info[2]}")
                        get_image_for_muscle_group(muscle)
                        st.write("##")

                    if info[2] == None:
                        st.markdown(f"##### [ {i+1} ] - {muscle}")
                        st.write("Modifier : Nope")
                        get_image_for_muscle_group(muscle)
                        st.write("##")
                
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

                        sets = 3 ## FIGURE OUT HOW THIS WILL WORK FFS - ALSO CONSIDER NOW PAGES AND MAYBE JUST DO WITH THAT AS CONTROL FLOW?

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
                                        print_timer(number)

                                    



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