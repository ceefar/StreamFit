from bs4 import BeautifulSoup as soup
import requests

main_url = "https://exrx.net"

def get_templates_to_display() -> dict:
    """ write me pls """
    # USE TO SELECT THE LEVEL/SPLIT THE USER WANTS
    url_1_lta = "https://exrx.net/Workouts/Workout1LTA" # 1 day - legs torso arms
    url_1_lpp = "https://exrx.net/Workouts/Workout1LPP" # 1 day - legs push pull
    url_1_pppp = "https://exrx.net/Workouts/Workout1PPPP" # 1 day - push pull stagger (ie push, pull, push, pull ?)
    url_1_ulul = "https://exrx.net/Workouts/Workout1ULUL" # 1 day - upper lower stagger (ie upper lower upper lower ?)
    url_2_pp = "https://exrx.net/Workouts/Workout2PP" # 2 day - push pull

    # OBVS DO AS FUNCTION AND MUCH BETTER, MAYBE EVEN DYNAMIC, BUT JUST DOING SIMPLE AF FOR NOW
    template_dict = {"Legs Torso Arms [1 DAY]":url_1_lta,"Legs Push Pull [1 DAY]":url_1_lpp,"Push Pull Stagger [1 DAY]":url_1_pppp,"Upper Lower Stagger [1 DAY]":url_1_ulul,"Push Pull [2 DAY]":url_2_pp}
    return(template_dict)

def get_data_from_url(url:str):
    # GET THE URL DATA
    result = requests.get(url)
    doc = soup(result.text, "html.parser")
    return(doc)

def get_sessions_from_pagedata(url) -> list:
    doc = get_data_from_url(url)
    # GET SESSIONS FROM URL DATA
    sessions_h3_tags = doc.find_all("h3")
    sessions_h3_tags.pop()
    sessions_h3_tags.pop()
    sessions_h3_tags_title = sessions_h3_tags[0]
    sessions_h3_tags.pop(0)
    sessions_h3_tags_title = str(sessions_h3_tags_title)
    sessions_h3_tags_title = sessions_h3_tags_title.replace("<h3>","")
    sessions_h3_tags_title = sessions_h3_tags_title.replace("</h3>","")
    session_list = []
    [session_list.append(session.text) for session in sessions_h3_tags]
    return(session_list)

def get_session_count(doc) -> int:
    session_count = []
    session_col_div_classes_counter = doc.find_all('div', {'class': 'col-sm-6'})
    [session_count.append(session) for session in session_col_div_classes_counter]
    return(session_count)

def get_base_template_info(user_wants_session, url) -> dict:
    doc = get_data_from_url(url)
    session_count = get_session_count(doc)
    session_dict = {}
    # T0DO PROPER - IS TOO H4CKY AF - GET SESSION FROM USER SELECTION
    for x in range(len(session_count)):
        session_col_div_classes = doc.find_all('div', {'class': 'col-sm-6'})[x]
        # OBVS IS A BETTER WAY TO DO THIS BUT JUST RUSHING IT OUT TO SEE WAGWAN
        if x == user_wants_session:
            #print(session_col_div_classes.text)
            for a in session_col_div_classes.find_all('a', href=True):
                name = (f"{a.text}")
                link = (a['href']) #f"{a.get('href')}"
                if name:
                    modifier = get_info_from_mg_parent(str(a.parent))
                    session_dict[name] = (link, str(a.parent), modifier)
                    
                    #print(a.parent)
                    #print(name)
                    #print(link)
                    #print(session_dict)
            return(session_dict)

def get_info_from_mg_parent(a_parent):
    #print(a_parent)
    mg_modifier = a_parent.find("♦")
    if mg_modifier > -1:
        #print("Choose Only Side Or Front Delt")
        return("Choose Only Side Or Front Delt")
    mg_modifier = a_parent.find("~")
    if mg_modifier > -1:
        #print("Choose Erector Spinae")
        return("Choose Erector Spinae")
    mg_modifier = a_parent.find("+")
    if mg_modifier > -1:
        #print("Choose Auxillary Abs")
        return("Choose Auxillary Abs")

        # OPTIONAL AND THIS IS DONE BAR FORMATTING FOR LINK
        # THEN JUST GET IMAGES OOO


def get_all_exercises_from_mg_triceps():
    """ gets exercise list with links, actually works perfectly fine for most pages, but there is no way for me to truly get
    sibling relationships due to poor formatting of list items, no classes assigned, and my lack of expert level regex
    that being said if you just need a list of all exercises (with no relational info) then this works fine """

    result = requests.get("https://exrx.net/Lists/ExList/ArmWt#Triceps") #("https://exrx.net/Lists/ExList/ChestWt#General")
    doc = soup(result.text, "html.parser")

    for a in doc.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href']) 

    end_index = str(doc).find("Exercise Lists")
    if end_index == -1:
        end_index = str(doc).find("Exercise List")
    doc2 = str(doc)[:end_index]
    doc2 = soup(doc2, "html.parser")

    for a in doc2.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href'])

    start_index = str(doc2).find("mainShell")
    doc3 = str(doc2)[start_index:]
    doc3 = soup(doc3, "html.parser")

    ex_plus_links_list = []

    for a in doc3.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href']) #f"{a.get('href')}"
        ex_plus_links_list.append((name,link))

        #print(f"{name = }")
        #print(f"{link = }")
        #print("##")

    doc4 = str(doc)[start_index:end_index]
    doc4 = soup(doc4, "html.parser")

    # can return doc4 too if needed btw

    ex_plus_links_list.pop()
    ex_plus_links_list.pop(0)
    ex_plus_links_list.pop(0)

    [print(tup) for tup in ex_plus_links_list]

    return(ex_plus_links_list)
    


def get_all_exercises_from_mg_chest():
    """ gets exercise list with links, actually works perfectly fine for most pages, but there is no way for me to truly get
    sibling relationships due to poor formatting of list items, no classes assigned, and my lack of expert level regex
    that being said if you just need a list of all exercises (with no relational info) then this works fine """

    result = requests.get("https://exrx.net/Lists/ExList/ChestWt#General")
    doc = soup(result.text, "html.parser")

    for a in doc.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href']) 

    end_index = str(doc).find("Exercise Lists")
    if end_index == -1:
        end_index = str(doc).find("Exercise List")
    doc2 = str(doc)[:end_index]
    doc2 = soup(doc2, "html.parser")

    for a in doc2.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href'])

    start_index = str(doc2).find("mainShell")
    doc3 = str(doc2)[start_index:]
    doc3 = soup(doc3, "html.parser")

    ex_plus_links_list = []

    for a in doc3.find_all('a', href=True):
        name = (f"{a.text}")
        link = (a['href']) #f"{a.get('href')}"
        ex_plus_links_list.append((name,link))

        #print(f"{name = }")
        #print(f"{link = }")
        #print("##")

    doc4 = str(doc)[start_index:end_index]
    doc4 = soup(doc4, "html.parser")

    # can return doc4 too if needed btw

    ex_plus_links_list.pop()
    ex_plus_links_list.pop(0)
    ex_plus_links_list.pop(0)

    [print(tup) for tup in ex_plus_links_list]

    return(ex_plus_links_list)
    
    


def program():
    template_dict = {}

    [print(f"[ {i+1} ] - {template}") for i, (template, _) in enumerate(template_dict.items())]

    # OWN FUNCTION, CHECK IS IN RANGE
    user_wants_template = int(input("\nSelect Your Template : "))

    # GET AND PRINT THE USERS SELECTION
    print("------------------------------------")
    for i, (template, link) in enumerate(template_dict.items()):
        if user_wants_template-1 == i:
            url = template_dict[template]
            print(f"Selected : {template}")
            print(f"Loading from {url}")
    print("------------------------------------")
    fakeinput = input("Press Enter To Continue : ")

    # GET THE URL DATA
    result = requests.get(url)
    doc = soup(result.text, "html.parser")

    # PRINT THE AMOUNT(count) OF SESSIONS TO CHOOSE FROM
    print("")
    session_count = []
    session_col_div_classes_counter = doc.find_all('div', {'class': 'col-sm-6'})
    [session_count.append(session) for session in session_col_div_classes_counter]
    print(f"{len(session_count)} SESSIONS FOUND")
    print("------------------------------------")

    # GET SESSIONS FROM URL DATA
    sessions_h3_tags = doc.find_all("h3")
    sessions_h3_tags.pop()
    sessions_h3_tags.pop()
    sessions_h3_tags_title = sessions_h3_tags[0]
    sessions_h3_tags.pop(0)
    sessions_h3_tags_title = str(sessions_h3_tags_title)
    sessions_h3_tags_title = sessions_h3_tags_title.replace("<h3>","")
    sessions_h3_tags_title = sessions_h3_tags_title.replace("</h3>","")
    print(sessions_h3_tags_title)
    print("------------------------------------")
    [print(session.text) for session in sessions_h3_tags]
    print("------------------------------------")

    # SELECT ONE AND PRINT OUT - NEEDS VALIDATION FROM FUNCTION - MAKE 1 FUNCTION TO VALIDATE AND PASS STUFF TO IT DUH!
    user_wants_session = int(input("\nSelect Your Session : "))
    print("")
    print("YOUR SESSION")
    print("------------------------------------")
    # T0DO PROPER - IS TOO H4CKY AF - GET SESSION FROM USER SELECTION
    for x in range(len(session_count)):
        session_col_div_classes = doc.find_all('div', {'class': 'col-sm-6'})[x]
        # OBVS IS A BETTER WAY TO DO THIS BUT JUST RUSHING IT OUT TO SEE WAGWAN
        if x == user_wants_session-1:
            #print(session_col_div_classes.text)
            for a in session_col_div_classes.find_all('a', href=True):
                name = (f"{a.text}")
                link = (f"{a.get('href')}")  # a['href']
                if name:
                    print(name)
                    print(link)

    print("------------------------------------")
    print("")


# driver... vrmmmm
if __name__=='__main__':
    #program() 
    get_all_exercises_from_mg_chest()


# THEN ON TO STREAMLIT AND IMPLEMENT IMAGES AND SIMPLE TRACKING OOOOO
    # - link will be used for shit like changing equipment
    # - but for first display you just go there, get the img, ig get any other info
    # - and then let track
    # - have timer initial setting be dynamic based on the info from the exercise info 


# FOR FULL LINKS!
# https://stackoverflow.com/questions/64079965/print-only-lines-in-html-with-a-href-within-a-divider-html-using-the-beaut


"""
li = doc.find('li', {'class': 'col-sm-6'})
children = li.findChildren("a" , recursive=False)
for child in children:
    print(child)
"""


