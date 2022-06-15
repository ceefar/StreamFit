# ---- imports ----
import random


# ---- functions start ----

def calculate_rest_time_v0(musclegroup:str, currentsplit:str) -> int:
    """ returns basic dynamic rest timings for given muscle group - v0.2 """
    large_muscles = ["Back, Back - Lats, Quadriceps, Hamstrings"] # urm just 1 list? idk what works best tbf but this is kinda dumb as is lol (as in could just be a string duh)
    medium_muscles = ["Chest", "Upper Chest", "Front Delt"]
    small_muscles = ["Calves, Biceps, Triceps, Abdominal, Forearms"]

    #print(f"{musclegroup = }")
    #print(f"{currentsplit = }")

    # some way to judge what plan it is - tbh just a better db column or even new column whatever - to dictate rest for now is fine
        # going by amount of days so 1 day split sure beginner u want rest but its a full body workout so time cant afford lots of rest
        # 2 day can stretch to more rest of certain things, doing this dynamically (& for lots of other variables too) will take serioius thought and planning ngl
    fullbody_splits = ["Chest, Back, Arms, Legs"]
    # obvs would use a users level as a metric as full body can even work for intermediate, again more considerations for dynamic var creation
    twoday_splits = [""]

    # determine the muscle, obvs then specifics by any modifiers to the plan/session, the equipment, user level, etc (even modifiers for target area too btw!)
    # if it has to be a big switch so be it but maybe is a way to do it programatically with multiplication modifiers idk?  
    # (or even just addition of X seconds if flag, with that secondAddition being different for each 'size' muscle group)

    # note keep these short for now, obvs scale them so is clear tho
    if currentsplit in fullbody_splits:
        if musclegroup in large_muscles:
            rest_timer = 12 # 120 sec
        elif musclegroup in medium_muscles:
            rest_timer = 9 # 90 sec, you get it...
        else:
            rest_timer = 6
    else:
        # for 2 day
        if musclegroup in large_muscles:
            rest_timer = 18 # 180 sec
        elif musclegroup in medium_muscles:
            rest_timer = 12 # 120 sec, you get it...
        else:
            rest_timer = 5

    return(rest_timer)


def get_real_world_weight_comparison(weight):
    """ write me pls ceef """

    # for now just choose a random one that is appropriate and return it
    # allow to choose a diff other random one
    # and share too

    # URM, PROBABLY JUST MAKE EM DICTIONARIES THEN DUH!
    light=[(10,"Chocolate Bar")]
    moderate=[(14,"Car Tire"),(20,"Karaoke Machine"),(25,"2 Year Old Toddler"),(40,"A Human Leg"),(80,"Head Of Giraffe"),(99,"A Flock Of Geese"),(181.43,"Whale Heart"),(250,"Jesus Christ")]
    # CONVERT ALL EXCEPT TIRE TO KG - actually doesnt matter rn tho
    heavy=[("Whale Heart",181.43)] # name, weight in kg, weight in lbs? (400 for whale btw)

    # so you basically just do this twice, once to find which bucket it is closest too by giving the buckets a different var thats their range (max ig)
    # then once you have the bucket you do the below bosh

    check_list = []
    [check_list.append(weight[0]) for weight in moderate]
    min_numb_result = (min(check_list, key=lambda x:abs(x-weight)))

    #print(f"{min_numb_result = }")

    find_result_dict = dict(moderate)
    find_result = find_result_dict[min_numb_result]

    #print(f"{find_result = }")

    multiplier:float = min_numb_result/weight

    #print(f"{multiplier = }")

    return((find_result,min_numb_result,multiplier)) # objects weight so ig could compare how close to that you are in a metric too? (can also do the x times too, mays well return in the tuple tbf)
    #return(("Object",1000,"1.5x"))


    # http://www.weightandthings.com/screens.php?p=67&u=kg
    # https://www.sparkpeople.com/blog/blog.asp?post=what_things_weigh_measure_your_progress_with_realworld_items
    # www.themeasureofthings.com/results.php?comp=weight&unit=lbs&amt=1500&sort=pr&p=1
    


get_real_world_weight_comparison(65)

