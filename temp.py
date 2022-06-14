
# SELECT ONE AND PRINT OUT - NEEDS VALIDATION FROM FUNCTION - MAKE 1 FUNCTION TO VALIDATE AND PASS STUFF TO IT DUH!
user_wants_session = int(input("\nSelect Your Session : "))

# T0DO PROPER - IS TOO H4CKY AF - GET SESSION FROM USER SELECTION
for x in range(len(session_count)):
    session_col_div_classes = doc.find_all('div', {'class': 'col-sm-6'})[x]
    # OBVS IS A BETTER WAY TO DO THIS BUT JUST RUSHING IT OUT TO SEE WAGWAN
    if x == user_wants_session-1:
        #print(session_col_div_classes.text)
        for a in session_col_div_classes.find_all('a', href=True):
            print(f"{a.text}", a['href'])

        muscle_groups = session_col_div_classes.find_all('li')
        for mg in muscle_groups:
            print(mg.text)
            mg_link = mg.find('a')
            print(mg_link.text)            
        
        muscle_group_links = session_col_div_classes.find_all('a')
        print(muscle_group_links)