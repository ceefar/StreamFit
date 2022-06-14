# main streamlit dashboard page
# imports 
# for web app
import streamlit as st
# for exrx websrape access
import integration_scrape_exrx as exrx
# for db access
import integration_database as fitdb

# ---- cached functions ----

@st.cache
def grab_templates_to_display() -> dict:
    templates = exrx.get_templates_to_display()
    return(templates)

@st.cache
def grab_sessions_from_pagedata(url):
    sessions_list = exrx.get_sessions_from_pagedata(url)
    return(sessions_list)

@st.cache
def grab_base_template_info(user_selection_int, url):
    session_dict = exrx.get_base_template_info(user_selection_int, url)
    return(session_dict)
      
@st.cache
def create_user_db_tables(user_name:str):
    fitdb.db_create_user(user_name)


# ---- main page ----

# FOR ONBOARDING AND BELOW FLOW 
# https://blog.streamlit.io/how-to-create-interactive-books-with-streamlit-and-streamlit-book-in-5-steps/

def run():
    # page config stuff
    st.set_page_config(
        page_title="Dashboard",
        page_icon=":sunglasses:", # :bar_chart:
    )
    # sidebar stuff
    st.sidebar.info("Select a page above.")
            
    # ---- calls and vars ----
    # EMPTY 

    # TOPPER container
    with st.container():
        st.title(f"Title :chart_with_upwards_trend:")
        st.write("---")

    # SHOW TEMPLATES container
    with st.container():
  
        st.markdown(f"""#### :calendar: Title """)
        st.write("##")

        # key = NAME:str, value = URL:idk? -> "Legs Torso Arms [1 DAY]":url_1_lta
        templates_dict = grab_templates_to_display()

        # have it default to user ig
        user_name = st.text_input('Enter Your Name', 'user')
        st.write('The current Username is', user_name)
        if st.checkbox('Create User Account'):
            create_user_db_tables(user_name)
            if "active_user" not in st.session_state:
                st.session_state["active_user"] = user_name

        store_selector = st.selectbox("Choose A Template", options=templates_dict.keys(), index=0)
        
        url = templates_dict[store_selector]

        st.write(f"{url}")

        st.write("##")

        page_sessions = grab_sessions_from_pagedata(url)
        selected_session = st.radio("Sessions", page_sessions)
        st.write(f"Selected Session -> {selected_session}")
        
        if st.checkbox('Make This The Live Session & See More Info'):
            try:
                selection_as_int = page_sessions.index(selected_session)
            except ValueError:
                st.write("Idk How You Managed To Make It Error... But You Made It Error")

            session_as_dict = grab_base_template_info(selection_as_int, url)

            if "session" not in st.session_state:
                st.session_state["session"] = session_as_dict
                st.session_state["session_name"] = selected_session
            else:
                st.session_state["session"] = session_as_dict
                st.session_state["session_name"] = selected_session
            
            st.write(session_as_dict)

        st.write("##")
        st.write("""### NOW GO TO WORKOUT! """)








if __name__ == "__main__":
    run()


