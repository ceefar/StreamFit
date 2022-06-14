from bs4 import BeautifulSoup as soup
import requests



# USE TO SELECT THE LEVEL/SPLIT THE USER WANTS
url_1_lta = "https://exrx.net/Workouts/Workout1LTA" # 1 day - legs torso arms
url_1_lpp = "https://exrx.net/Workouts/Workout1LPP" # 1 day - legs push pull
url_1_pppp = "https://exrx.net/Workouts/Workout1PPPP" # 1 day - push pull stagger (ie push, pull, push, pull ?)
url_1_ulul = "https://exrx.net/Workouts/Workout1ULUL" # 1 day - upper lower stagger (ie upper lower upper lower ?)
url_2_pp = "https://exrx.net/Workouts/Workout2PP" # 2 day - push pull

# OBVS DO AS FUNCTION AND MUCH BETTER, MAYBE EVEN DYNAMIC, BUT JUST DOING SIMPLE AF FOR NOW
template_dict = {"Legs Torso Arms [1 DAY]":url_1_lta,"Legs Push Pull [1 DAY]":url_1_lpp,"Push Pull Stagger [1 DAY]":url_1_pppp,"Upper Lower Stagger [1 DAY]":url_1_ulul,"Push Pull [2 DAY]":url_2_pp}
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("TEMPLATE OPTIONS")
print("------------------------------------")
[print(f"[ {i+1} ] - {template}") for i, (template, _) in enumerate(template_dict.items())]
print("------------------------------------")

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


