import csv
from gmplot import gmplot
import copy

### Bike Share Project Phase 1 ### 
### Yuxiang Chen, JunHwa Lee, Jaehyung Rhee, Chloe Yoo ### 

### CHANGE DIRECTORY BELOW ### 
DP_data = "/Users/junhwalee/Desktop/project1/Data/BS_DP_small.csv"  ### CHANGE HERE
PL_data = "/Users/junhwalee/Desktop/project1/Data/BS_PL_small.csv"  ### CHANGE HERE
MUN_data = "/Users/junhwalee/Desktop/project1/Data/BS_MUN_small.csv" ### CHANGE HERE
####################################
############### FUNCTION LIST For Part 1 ############### 
def parse_csv(path):
    ## parse_csv reads out csv line by line
    with open(path,'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            yield row

def max_distance_finder(DP_DP_distance) : 
    ## max_distance_finder goes through each value inside DP_DP_distance and 
    ## returns maximum value in DP_DP_distance and where(in what two DPs) that maximum distance occurs
    max_distance = 0 
    max_distance_location = [0, 0]
    for pos1, val1 in enumerate(DP_DP_distance) : 
        if pos1 == 0 :
            max_distance = max(val1)
        else : 
            max_distance = max([max_distance, max(val1)])
            if max_distance == max(val1) : 
                max_distance_location = [pos1, val1.index(max_distance)]
    return [max_distance, max_distance_location]

def time_calculate(PLs_near_first_DP, PLs_near_second_DP) :
    ## time_calculate calculates times that takes to move 
    ## from chosen path of (first_DP -> first point in PLs_near_first_DP -> first point in PLs_near_second_DP -> second_DP)
    time = (PLs_near_first_DP[0][1] + PLs_near_second_DP[0][1]) / 3 + PL_PL_distance[PLs_near_first_DP[0][0]][PLs_near_second_DP[0][0]] / 15 
    return time

## Following 4 functions are basically same but they are made into 4 different functions based on location relationships between first_DP and second_DP
def lat_bigger_s_long_bigger_f() : 
    ## case when second_DP has larger latitude than first_DP & first_DP has larger longitude than second_DP
    # getting all PLs near first_DP
    PLs_near_first_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_first_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_first_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[first_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) and (PL_pos[pos][1] >= second_coordinates[1]): 
            PLs_near_first_DP_priorityA = PLs_near_first_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1])) or ((PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]))): 
            PLs_near_first_DP_priorityB = PLs_near_first_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_first_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_first_DP_priorityA = sorted(PLs_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True) # ordering PLs in region A 
    PLs_near_first_DP_priorityB = sorted(PLs_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True) # ordering PLs in region B
    PLs_near_first_DP_priorityC = sorted(PLs_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True) # ordering PLs in region C
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_first_DP_priorityC[pos3] 
    # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_first_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)
    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_first_DP_priorityA = PLs_existing_near_first_DP_priorityA + [val1]
                    del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_first_DP_priorityB = PLs_existing_near_first_DP_priorityB + [val2]
                    del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_first_DP_priorityC = PLs_existing_near_first_DP_priorityC + [val3]
                    del PLs_near_first_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_first_DP_priorityA = sorted(PLs_existing_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityB = sorted(PLs_existing_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityC = sorted(PLs_existing_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_first_DP = PLs_existing_near_first_DP_priorityA + PLs_existing_near_first_DP_priorityB + PLs_existing_near_first_DP_priorityC
    PLs_near_first_DP = sorted(PLs_existing_near_first_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_first_DP_priorityA + PLs_near_first_DP_priorityB + PLs_near_first_DP_priorityC
    global original_PLs_existing_near_first_DP
    original_PLs_existing_near_first_DP = copy.deepcopy(PLs_near_first_DP)
    print("===========================================================================")
    print("sf Possible PLs near first DP (PL number, distance from that PL to DP) : " +str(PLs_near_first_DP) )
    
    # getting all PLs near second_DP
    PLs_near_second_DP_priorityA = [] # PLs in region A of figure in 2 page memo
    PLs_near_second_DP_priorityB = [] # PLs in region B of figure in 2 page memo
    PLs_near_second_DP_priorityC = [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[second_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) and (PL_pos[pos][1] >= second_coordinates[1]):  
            PLs_near_second_DP_priorityA = PLs_near_second_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1])) or ((PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1]))): 
            PLs_near_second_DP_priorityB = PLs_near_second_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_second_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_second_DP_priorityA = sorted(PLs_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityB = sorted(PLs_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityC = sorted(PLs_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible"
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : 
                    del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : 
                    del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : 
                    del PLs_near_second_DP_priorityC[pos3]
    # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_second_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)
    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_second_DP_priorityA = PLs_existing_near_second_DP_priorityA + [val1]
                    del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_second_DP_priorityB = PLs_existing_near_second_DP_priorityB + [val2]
                    del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_second_DP_priorityC = PLs_existing_near_second_DP_priorityC + [val3]
                    del PLs_near_second_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_second_DP_priorityA = sorted(PLs_existing_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityB = sorted(PLs_existing_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityC = sorted(PLs_existing_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)

    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_second_DP = PLs_existing_near_second_DP_priorityA + PLs_existing_near_second_DP_priorityB + PLs_existing_near_second_DP_priorityC
    PLs_near_second_DP = sorted(PLs_existing_near_second_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_second_DP_priorityA + PLs_near_second_DP_priorityB + PLs_near_second_DP_priorityC
    global original_PLs_existing_near_second_DP
    original_PLs_existing_near_second_DP = copy.deepcopy(PLs_near_second_DP)
    print("sf Possible PLs near second DP (PL number, distance from that PL to DP) : " +str(PLs_near_second_DP) +"\n")
    # return two lists of PLs that are near each DP 
    return [PLs_near_first_DP,PLs_near_second_DP]

def lat_bigger_s_long_bigger_s() :
    ## case when second_DP has larger latitude and larger longitude than first_DP 
    # getting all PLs near first_DP
    PLs_near_first_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_first_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_first_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[first_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) and (PL_pos[pos][1] <= second_coordinates[1]): 
            PLs_near_first_DP_priorityA = PLs_near_first_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1])) or ((PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]))): 
            PLs_near_first_DP_priorityB = PLs_near_first_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_first_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_first_DP_priorityA = sorted(PLs_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityB = sorted(PLs_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityC = sorted(PLs_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_first_DP_priorityC[pos3]
    # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_first_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)
    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_first_DP_priorityA = PLs_existing_near_first_DP_priorityA + [val1]
                    del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_first_DP_priorityB = PLs_existing_near_first_DP_priorityB + [val2]
                    del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_first_DP_priorityC = PLs_existing_near_first_DP_priorityC + [val3]
                    del PLs_near_first_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_first_DP_priorityA = sorted(PLs_existing_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityB = sorted(PLs_existing_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityC = sorted(PLs_existing_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_first_DP = PLs_existing_near_first_DP_priorityA + PLs_existing_near_first_DP_priorityB + PLs_existing_near_first_DP_priorityC
    PLs_near_first_DP = sorted(PLs_existing_near_first_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_first_DP_priorityA + PLs_near_first_DP_priorityB + PLs_near_first_DP_priorityC
    global original_PLs_existing_near_first_DP
    original_PLs_existing_near_first_DP = copy.deepcopy(PLs_near_first_DP)
    print("===========================================================================")
    print("ss Possible PLs near first DP (PL number, distance from that PL to DP) : " +str(PLs_near_first_DP))

    # getting all PLs near second_DP
    PLs_near_second_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_second_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_second_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[second_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) and (PL_pos[pos][1] <= second_coordinates[1]):  
            PLs_near_second_DP_priorityA = PLs_near_second_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1])) or ((PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1]))): 
            PLs_near_second_DP_priorityB = PLs_near_second_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_second_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_second_DP_priorityA = sorted(PLs_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityB = sorted(PLs_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityC = sorted(PLs_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_second_DP_priorityC[pos3]
     # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_second_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)
    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_second_DP_priorityA = PLs_existing_near_second_DP_priorityA + [val1]
                    del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_second_DP_priorityB = PLs_existing_near_second_DP_priorityB + [val2]
                    del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_second_DP_priorityC = PLs_existing_near_second_DP_priorityC + [val3]
                    del PLs_near_second_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_second_DP_priorityA = sorted(PLs_existing_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityB = sorted(PLs_existing_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityC = sorted(PLs_existing_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
   
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_second_DP = PLs_existing_near_second_DP_priorityA + PLs_existing_near_second_DP_priorityB + PLs_existing_near_second_DP_priorityC
    PLs_near_second_DP = sorted(PLs_existing_near_second_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_second_DP_priorityA + PLs_near_second_DP_priorityB + PLs_near_second_DP_priorityC
    global original_PLs_existing_near_second_DP
    original_PLs_existing_near_second_DP = copy.deepcopy(PLs_near_second_DP)
    print("ss Possible PLs near second DP (PL number, distance from that PL to DP) : " +str(PLs_near_second_DP) +"\n")
    # return two lists of PLs that are near each DP 
    return [PLs_near_first_DP,PLs_near_second_DP]

def lat_bigger_f_long_bigger_s() : 
    ## case when first_DP has larger latitude than second_DP & second_DP has larger longitude than first_DP
    # getting all PLs near first_DP
    PLs_near_first_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_first_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_first_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[first_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) and (PL_pos[pos][1] <= second_coordinates[1]): 
            PLs_near_first_DP_priorityA = PLs_near_first_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1])) or ((PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]))): 
            PLs_near_first_DP_priorityB = PLs_near_first_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_first_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest 
    PLs_near_first_DP_priorityA = sorted(PLs_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityB = sorted(PLs_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityC = sorted(PLs_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : 
                    del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : 
                    del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : 
                    del PLs_near_first_DP_priorityC[pos3]
    # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_first_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)

    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_first_DP_priorityA = PLs_existing_near_first_DP_priorityA + [val1]
                    del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_first_DP_priorityB = PLs_existing_near_first_DP_priorityB + [val2]
                    del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_first_DP_priorityC = PLs_existing_near_first_DP_priorityC + [val3]
                    del PLs_near_first_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_first_DP_priorityA = sorted(PLs_existing_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityB = sorted(PLs_existing_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityC = sorted(PLs_existing_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_first_DP = PLs_existing_near_first_DP_priorityA + PLs_existing_near_first_DP_priorityB + PLs_existing_near_first_DP_priorityC
    PLs_near_first_DP = sorted(PLs_existing_near_first_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_first_DP_priorityA + PLs_near_first_DP_priorityB + PLs_near_first_DP_priorityC
    global original_PLs_existing_near_first_DP
    original_PLs_existing_near_first_DP = copy.deepcopy(PLs_near_first_DP)
    print("===========================================================================")
    print("fs Possible PLs near first DP (PL number, distance from that PL to DP) : " +str(PLs_near_first_DP) )

    # getting all PLs near second_DP
    PLs_near_second_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_second_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_second_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[second_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) and (PL_pos[pos][1] <= second_coordinates[1]):  
            PLs_near_second_DP_priorityA = PLs_near_second_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1])) or ((PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1]))): 
            PLs_near_second_DP_priorityB = PLs_near_second_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_second_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_second_DP_priorityA = sorted(PLs_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityB = sorted(PLs_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityC = sorted(PLs_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) :
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_second_DP_priorityC[pos3] 
    # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_second_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)

    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_second_DP_priorityA = PLs_existing_near_second_DP_priorityA + [val1]
                    del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_second_DP_priorityB = PLs_existing_near_second_DP_priorityB + [val2]
                    del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_second_DP_priorityC = PLs_existing_near_second_DP_priorityC + [val3]
                    del PLs_near_second_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_second_DP_priorityA = sorted(PLs_existing_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityB = sorted(PLs_existing_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityC = sorted(PLs_existing_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_second_DP = PLs_existing_near_second_DP_priorityA + PLs_existing_near_second_DP_priorityB + PLs_existing_near_second_DP_priorityC
    PLs_near_second_DP = sorted(PLs_existing_near_second_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_second_DP_priorityA + PLs_near_second_DP_priorityB + PLs_near_second_DP_priorityC
    global original_PLs_existing_near_second_DP
    original_PLs_existing_near_second_DP = copy.deepcopy(PLs_near_second_DP)
    print("fs Possible PLs near second DP (PL number, distance from that PL to DP) : " +str(PLs_near_second_DP) +"\n")
    # return two lists of PLs that are near each DP
    return [PLs_near_first_DP,PLs_near_second_DP]

def lat_bigger_f_long_bigger_f() : 
    ## case when first_DP has larger latitude and larger longitude than second_DP 
    # getting all PLs near first_DP
    PLs_near_first_DP_priorityA= [] # PLs in region A of figure in 2 page memo
    PLs_near_first_DP_priorityB= [] # PLs in region B of figure in 2 page memo
    PLs_near_first_DP_priorityC= [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[first_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) and (PL_pos[pos][1] >= second_coordinates[1]): 
            PLs_near_first_DP_priorityA = PLs_near_first_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1])) or ((PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]))): 
            PLs_near_first_DP_priorityB = PLs_near_first_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] >= first_coordinates[0]) and (PL_pos[pos][1] >= first_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_first_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_first_DP_priorityA = sorted(PLs_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityB = sorted(PLs_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_first_DP_priorityC = sorted(PLs_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible" 
    for pos, val in enumerate(PL_vector) : 
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_first_DP_priorityC[pos3]
     # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_first_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_first_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)

    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_first_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_first_DP_priorityA = PLs_existing_near_first_DP_priorityA + [val1]
                    del PLs_near_first_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_first_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_first_DP_priorityB = PLs_existing_near_first_DP_priorityB + [val2]
                    del PLs_near_first_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_first_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_first_DP_priorityC = PLs_existing_near_first_DP_priorityC + [val3]
                    del PLs_near_first_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_first_DP_priorityA = sorted(PLs_existing_near_first_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityB = sorted(PLs_existing_near_first_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_first_DP_priorityC = sorted(PLs_existing_near_first_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_first_DP = PLs_existing_near_first_DP_priorityA + PLs_existing_near_first_DP_priorityB + PLs_existing_near_first_DP_priorityC
    PLs_near_first_DP = sorted(PLs_existing_near_first_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_first_DP_priorityA + PLs_near_first_DP_priorityB + PLs_near_first_DP_priorityC
    global original_PLs_existing_near_first_DP
    original_PLs_existing_near_first_DP = copy.deepcopy(PLs_near_first_DP)
    print("===========================================================================")
    print("ff Possible PLs near first DP (PL number, distance from that PL to DP) : " +str(PLs_near_first_DP))

    # getting all PLs near second_DP
    PLs_near_second_DP_priorityA = [] # PLs in region A of figure in 2 page memo
    PLs_near_second_DP_priorityB = [] # PLs in region B of figure in 2 page memo
    PLs_near_second_DP_priorityC = [] # PLs in region C of figure in 2 page memo
    for pos, val in enumerate(DP_PL_distance[second_DP]) : 
        if (val <= 1) and (PL_pos[pos][0] <= first_coordinates[0]) and (PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] <= first_coordinates[1]) and (PL_pos[pos][1] >= second_coordinates[1]):  
            PLs_near_second_DP_priorityA = PLs_near_second_DP_priorityA +[(pos,val)]
        elif (val <= 1) and (((PL_pos[pos][0] >= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1])) or ((PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] >= second_coordinates[1]))): 
            PLs_near_second_DP_priorityB = PLs_near_second_DP_priorityB +[(pos,val)]
        elif (val <= 1) and (PL_pos[pos][0] <= second_coordinates[0]) and (PL_pos[pos][1] <= second_coordinates[1]) : 
            PLs_near_first_DP_priorityC = PLs_near_second_DP_priorityC +[(pos,val)]
    # ordering PLs in each region from farthest from first_DP to closest
    PLs_near_second_DP_priorityA = sorted(PLs_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityB = sorted(PLs_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_near_second_DP_priorityC = sorted(PLs_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    # eliminating PLs that are marked as "not possible"
    for pos, val in enumerate(PL_vector) :
        if val == -1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : del PLs_near_second_DP_priorityC[pos3]
     # separating PLs that are already fixed (in other words, PLs that have PL_vector = 1)    
    PLs_existing_near_second_DP_priorityA = [] # PLs that already exist in region A of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityB = [] # PLs that already exist in region B of figure in 2 page memo (in other words, PL_vector value = 1)
    PLs_existing_near_second_DP_priorityC = [] # PLs that already exist in region C of figure in 2 page memo (in other words, PL_vector value = 1)

    for pos, val in enumerate(PL_vector) : 
        if val == 1 : 
            for pos1, val1 in enumerate(PLs_near_second_DP_priorityA) : 
                if pos == val1[0] : 
                    PLs_existing_near_second_DP_priorityA = PLs_existing_near_second_DP_priorityA + [val1]
                    del PLs_near_second_DP_priorityA[pos1]
            for pos2, val2 in enumerate(PLs_near_second_DP_priorityB) : 
                if pos == val2[0] : 
                    PLs_existing_near_second_DP_priorityB = PLs_existing_near_second_DP_priorityB + [val2]
                    del PLs_near_second_DP_priorityB[pos2]
            for pos3, val3 in enumerate(PLs_near_second_DP_priorityC) : 
                if pos == val3[0] : 
                    PLs_existing_near_second_DP_priorityC = PLs_existing_near_second_DP_priorityC + [val3]
                    del PLs_near_second_DP_priorityC[pos3]
    # sorting PLs that are already fixed from farthest to closest
    PLs_existing_near_second_DP_priorityA = sorted(PLs_existing_near_second_DP_priorityA, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityB = sorted(PLs_existing_near_second_DP_priorityB, key = lambda tup: tup[1], reverse= True)
    PLs_existing_near_second_DP_priorityC = sorted(PLs_existing_near_second_DP_priorityC, key = lambda tup: tup[1], reverse= True)
    
    # combining lists of PLs so that it will end up with PLs_near_first_DP which has ordered list of PLs based on priority mentioned in 2 page memo
    PLs_existing_near_second_DP = PLs_existing_near_second_DP_priorityA + PLs_existing_near_second_DP_priorityB + PLs_existing_near_second_DP_priorityC
    PLs_near_second_DP = sorted(PLs_existing_near_second_DP, key = lambda tup: tup[1], reverse= True) + PLs_near_second_DP_priorityA + PLs_near_second_DP_priorityB + PLs_near_second_DP_priorityC
    global original_PLs_existing_near_second_DP
    original_PLs_existing_near_second_DP = copy.deepcopy(PLs_near_second_DP)
    print("ff Possible PLs near second DP (PL number, distance from that PL to DP) : " +str(PLs_near_second_DP) +"\n")
    # return two lists of PLs that are near each DP 
    return [PLs_near_first_DP,PLs_near_second_DP]
## End of 4 similar functions ##  

def get_fixed_points(PLs_near_first_DP, PLs_near_second_DP) : 
    ## get_fixed_points goes through combinations of points in PLs_near_first_DP and PLs_near_second_DP and calculate time
    ## If time is less than 45 minutes, two PLs used in those calculations are fixed. 
    time = time_calculate(PLs_near_first_DP, PLs_near_second_DP)
    print("calculated time = " + str(time))
    if time <= 3/4 : print("Congratulation. Time is less than 45 min \n")
    else : # when time is over 45 minutes
        print("Time is over 45 min. \n")
        if (len(PLs_near_second_DP) != 1) and (len(PLs_near_first_DP) != 1) :
            if (PLs_near_first_DP[1][1] >= PLs_near_second_DP[1][1]) : 
                del PLs_near_first_DP[0]
                print("updated PLs_near_first_DP : " + str(PLs_near_first_DP)) 
            else : 
                del PLs_near_second_DP[0]
                print("updated PLs_near_second_DP : " + str(PLs_near_second_DP))
        # if there is only one remaining element, do not remove element from that list but remove element from another list 
        elif (len(PLs_near_second_DP) != 1) and (len(PLs_near_first_DP) == 1) :         
            del PLs_near_second_DP[0]
            print("updated PLs_near_second_DP : " + str(PLs_near_second_DP))
        # if there is only one remaining element, do not remove element from that list but remove element from another list
        elif (len(PLs_near_second_DP) == 1) and (len(PLs_near_first_DP) != 1) : 
            del PLs_near_first_DP[0]
            print("updated PLs_near_first_DP : " + str(PLs_near_first_DP))
        # when both lists end up with one element but if those elements do not end up creating path less than 45 minutes,
        # go through combination of PLs_near_first_DP and PLs_near_second_DP to find a combination that satisfy time constraint 
        else : #(len(PLs_near_first_DP) == 1) and (len(PLs_near_second_DP) == 1) 
            print("this should not happen")  
            PLs_near_first_DP, PLs_near_second_DP = copy.deepcopy(original_PLs_existing_near_first_DP), copy.deepcopy(original_PLs_existing_near_second_DP)
            if PLs_near_first_DP[0][1] >= PLs_near_second_DP[0][1] : # when first element of PLs_near_first_DP has greater distance value
                for pos1, val1 in enumerate(PLs_near_first_DP) : 
                    for pos2, val2 in enumerate(PLs_near_second_DP) : 
                        print(val2)
                        if time_calculate([val1],[val2]) <= 3/4 : 
                            return [pos1, val1]
            else  : # PLs_near_first_DP[0][1] < PLs_near_second_DP[0][1] : / # when first element of PLs_near_first_DP has greater distance value
                for pos1, val1 in enumerate(PLs_near_second_DP) : 
                    for pos2, val2 in enumerate(PLs_near_first_DP) : 
                        print(val2)
                        if time_calculate([val1],[val2]) <= 3/4 : 
                            return [pos1, val1]
        get_fixed_points(PLs_near_first_DP, PLs_near_second_DP)
    return [PLs_near_first_DP[0], PLs_near_second_DP[0]]

############### IMPORTING AND ORGANIZING DATA ###############
### Calculating number of DPs and number of PLs from data 
## 1) DP_number : number of DPs 
DP_number = 0 
for row in parse_csv(DP_data):
    DP_number = DP_number + 1 
DP_number = DP_number - 1
print("total number of DP : "+str(DP_number))
## 2) PL_number : number of PLs
for row in parse_csv(PL_data):
    PL_number = len(row)-DP_number - 5
    break
print("total number of PL : "+str(PL_number))
## 3) PL_vector : list with "PL_number" elements (i.e. if PL_number = 3, PL_vector has 3 elements)
PL_vector = [0 for x in range(PL_number)]
###########################################################################
### Importing and organizing distance and position data of DP and PL from data
## 1) DP_DP_distance : distance between one DP and another DP 
## DP_DP_distance : a list with DP_number elements / each element : a list with DP_number elements
DP_DP_distance = [[0 for x in range(DP_number)] for y in range(DP_number)]
i=-1
for row in parse_csv(DP_data) : 
    if i != -1 : 
        DP_DP_distance[i]= [float(x) for x in row[3:3+DP_number]]
    i = i+1 
original_DP_DP_distance = copy.deepcopy(DP_DP_distance)
## 2) PL_PL_distance : distance between one PL and another PL 
## PL_PL_distance : a list with PL_number elements / each element : a list with PL_number elements
PL_PL_distance = [[0 for x in range(PL_number)] for y in range(PL_number)]
i=-1
for row in parse_csv(PL_data) : 
    if i != -1 : 
        PL_PL_distance[i]= [float(x) for x in row[5:5+PL_number]]
    i = i+1 
## 3) PL_DP_distance : distance between PL and DP
## PL_DP_distance : a list with PL_number elements / each element : a list with DP_number elements
PL_DP_distance = [[0 for x in range(DP_number)] for y in range(PL_number)]
i=-1
for row in parse_csv(PL_data) : 
    if i != -1 : 
        PL_DP_distance[i]= [float(x) for x in row[5+PL_number:len(row)]]
    i = i+1 
## 4) DP_PL_distance : same information with 3) but flipped(transposed) (made this for future convenience)
## DP_PL_distance : a list with DP_number elements / each element : a list with PL_number elements
DP_PL_distance = [[3 for x in range(PL_number)] for y in range(DP_number)]
i = -1 
for row in parse_csv(PL_data) :
    if i != -1 : 
        for j in range(DP_number) : 
            DP_PL_distance[j][i] = float(row[5+PL_number+j])
    i = i +1
## 5) PL_pos : latitude and longitude of each PL  
## PL_pos : a list with PL_number elements / each element : [latitude, longitude of each PL]
PL_pos = [[0,0] for y in range(PL_number)]
i = -1 
for row in parse_csv(PL_data) : 
    if i != -1 : 
        PL_pos[i] = [float(x) for x in row[1:3]]
    i = i+1  
## 6) DP_pos : latitude and longitude of each DP 
## DP_pos : a list with PL_number elements / each element : [latitude, longitude of each DP]
DP_pos = [[0,0] for y in range(DP_number)]
i = -1 
for row in parse_csv(DP_data) : 
    if i != -1 : 
        DP_pos[i] = [float(x) for x in row[1:3]]
    i = i+1 
## 7) PL_extra : assigned municipality and whether that PL is PL is special or not 
## PL_extra : a list with PL_number elements / each element : [municipality number, special or not] (if special, then value is 1 / if not, value is 0)
PL_extra = [[0,0] for y in range(PL_number)]
i = -1 
for row in parse_csv(PL_data) : 
    if i != -1 : 
        PL_extra[i] = [float(x) for x in row[3:5]]
    i = i+1  
###########################################################################
### Importing and organizing data for municipalities 
## 1) MUN_number : number of municipalities
MUN_number = 0 
for row in parse_csv(MUN_data): MUN_number = MUN_number + 1 
MUN_number = int((MUN_number - 1)/2)
print("total number of MUN : "+str(MUN_number)+"\n")
## 2) MUN_minmax : minimum and maximum number of bikes for each municipality
## MUN_minmax : a list of MUN_number elements / each element : [minimum number, maximum number of bikes for each municipality]
MUN_minmax = [[0,0] for y in range(MUN_number)]
i = -1 
for row in parse_csv(MUN_data) : 
    if (i != -1) and (i%2 != 0) : 
        MUN_minmax[int((i-1)/2)] =[float(x) for x in row[1:3]]
    i = i+1 

############### PART 1 ###############
### STEP 1 : delete cases when DP_DP_distance is less than or equal to 9/4 miles(DP combinations where one person can walk from another DP in 45 minutes)
for pos1, val1 in enumerate(DP_DP_distance) : 
    for pos2, val2 in enumerate(val1) : 
        if val2 <= 3/4 * 3 : DP_DP_distance[pos1][pos2], DP_DP_distance[pos2][pos1] = 0, 0  
        # assign both to 0 since element in DP_DP_distance is redundant and symmetrical to diagonal line

### STEP 2 : Find two DPS that are farthest apart(variable : first_DP, second_DP) and make lists of PLs that are within 1 mile from each DP. 
## Find two DPS that are farthest apart
[max_distance, max_distance_location] = max_distance_finder(DP_DP_distance)
global original_PLs_existing_near_first_DP
global original_PLs_existing_near_second_DP
count = 0 # count : a variable that counts how many times the program goes through while loop below

while max_distance != 0 :  
    count = count + 1
    print("===========================================================================")
    print("LOOP "+str(count))
    print("current maximum distance = " + str(max_distance))
    first_DP = max_distance_location[0] # first_DP : DP number of first DP that creates the farthest distance
    second_DP = max_distance_location[1] # second_DP : DP number of second DP that creates the farthest distance
    print("and corresponding DP locations = " + str(first_DP)+ " & " + str(second_DP)) 
    first_coordinates = DP_pos[first_DP] # [latitude, longitude] of first_DP
    second_coordinates = DP_pos[second_DP] # [latitude, longitude] of second_DP
    # comparing latitude of first_DP and second_DP / if second one is bigger, which_lat_bigger = "s", if not, which_lat_bigger = "f"
    if first_coordinates[0] <= second_coordinates[0] : which_lat_bigger = "s"
    else : which_lat_bigger = "f"
    # comparing longitude of first_DP and second_DP / if second one is bigger, which_long_bigger = "s", if not, which_long_bigger = "f"
    if first_coordinates[1] <= second_coordinates[1] : which_long_bigger = "s"
    else : which_long_bigger = "f"

## Create ordered list of PLs near first_DP and second_DP (based on which_lat_bigger, which long bigger)
    if (which_lat_bigger == "s") and (which_long_bigger =="f"):
        [PLs_near_first_DP, PLs_near_second_DP] = lat_bigger_s_long_bigger_f()
    elif (which_lat_bigger == "s") and (which_long_bigger == "s") : 
        [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_s_long_bigger_s()
    elif (which_lat_bigger == "f") and (which_long_bigger == "s") : 
        [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_f_long_bigger_s()
    elif (which_lat_bigger == "f") and (which_long_bigger == "f") : 
        [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_f_long_bigger_f()

### STEP 3 : Fix two PLs by calculating time
    # first_fixed_PL : (PL number of PL that makes path from first_DP to second_DP less than 45 minutes, distance from this PL to first_DP)
    # second_fixed_PL : (PL_number of PL that makes path from first_DP to second_DP less than 45 minutes, distance from this PL to second_DP)
    [first_fixed_PL, second_fixed_PL] = get_fixed_points(PLs_near_first_DP, PLs_near_second_DP) 
    print("=====TWO PLs FIXED=====")
    print("Fixed First PL : " + str(first_fixed_PL) + " / Fixed Second PL : " + str(second_fixed_PL))
    # set DP_DP_distance of first_DP and second_DP to 0 since we finished considering that case
    DP_DP_distance[first_DP][second_DP] = 0 
    DP_DP_distance[second_DP][first_DP] = 0 

### STEP 4 : Make lists of PLs that are within 0.25 miles from first_fixed_PL and second_fixed_PL 
## When both that element and PL1/PL2 are not special PLs, change that element’s value in PL_vector to -1.
## (-1 means that that PL is no longer possible to have bike station)
## Change first_fixed_PL and second_fixed_PL's PL_vector to 1. 
    PLs_near_first_PL = [] # all PLs(including first_fixed_PL) that are inside 0.25 radius with center of first_fixed_PL 
    for index, value in enumerate(PL_PL_distance[first_fixed_PL[0]]) : 
        if value <= 0.25 : PLs_near_first_PL = PLs_near_first_PL + [(index,value)]
    print("All PLs near first fixed PL : "+ str(PLs_near_first_PL))
    for pos, val in PLs_near_first_PL : # going through each element in PLs_near_first_PL
        if pos != first_fixed_PL[0] :
            if PL_extra[pos][1] == 0 and PL_extra[first_fixed_PL[0]][0] == 0 : 
                PL_vector[pos]= -1 # change element of PL_vector to -1, when at least one of first_fixed_PL and another PL is not special
        else : PL_vector[first_fixed_PL[0]] = 1 # set element of PL_vector to 1 if corresponding PL is fixed
    PLs_near_second_PL = [] # all PLs(including second_fixed_PL) that are inside 0.25 radius with center of second_fixed_PL 
    for index, value in enumerate(PL_PL_distance[second_fixed_PL[0]]) : 
        if value <= 0.25 : PLs_near_second_PL = PLs_near_second_PL + [(index,value)]
    print("All PLs near second fixed PL : "+ str(PLs_near_second_PL))
    for pos, val in PLs_near_second_PL : # going through each element in PLs_near_second_PL
        if pos != second_fixed_PL[0] :
            if PL_extra[pos][1] == 0 and PL_extra[second_fixed_PL[0]][0] == 0 : 
                PL_vector[pos]= -1 # change element of PL_vector to -1, when at least oen of second_fixed_PL and another PL is not special
        else : PL_vector[second_fixed_PL[0]] = 1  # set element of PL_vector to 1 if corresponding PL is fixed
    
    print("\nupdated PL_vector : "+str(PL_vector))

### STEP 5 : Remove cases of DPs that are near fixed PLs that are within (DP1 to PL1 distance) from DP1 and (DP2 to PL2 distance) from DP2. 
### Then, since combinations of DPs in those lists are reachable within 45 minutes, change those cases' DP_DP_distance to 0. 
    DPs_near_first_fixed_PL = [] # list of all DPs that are inside radius of (distance between first_DP and first_fixed_PL) with first_fixed_PL as a center
    for pos, val in enumerate(PL_DP_distance[first_fixed_PL[0]]) :
        if val <= first_fixed_PL[1] : DPs_near_first_fixed_PL = DPs_near_first_fixed_PL + [(pos,val)]
    print("excluded DPs that are near first DP : " +str(DPs_near_first_fixed_PL)) 
    
    DPs_near_second_fixed_PL = [] # list of all DPs that are inside radius of (distance between second_DP and second_fixed_PL) with second_fixed_PL as a center
    for pos, val in enumerate(PL_DP_distance[second_fixed_PL[0]]) :
        if val <= second_fixed_PL[1] : DPs_near_second_fixed_PL = DPs_near_second_fixed_PL + [(pos,val)]
    print("excluded DPs that are near second DP : " +str(DPs_near_second_fixed_PL))
    
    # go through all possible combinations of DPs_near_first_fixed_PL and DPs_near_second_fixed_PL and change corresponding DP_DP_distance to 0
    for pos, val in enumerate(DPs_near_first_fixed_PL) : 
        for pos1, val1 in enumerate(DPs_near_second_fixed_PL) : 
            DP_DP_distance[val[0]][val1[0]]=0
            DP_DP_distance[val1[0]][val[0]]=0
    print("end of loop number "  + str(count)+"\n\n")
### STEP 6 : Find two DPS that are farthest apart. 
## if max_distance is not equal to 0, while loop will run again / if not, move on to Part 2
    [max_distance, max_distance_location] = max_distance_finder(DP_DP_distance) 

DP_checker = [0 for x in range(DP_number)]
for pos1, val1 in enumerate(PL_vector) : 
    if val1 == 1 : 
        for pos2, val2 in enumerate(DP_checker) : 
            if PL_DP_distance[pos1][pos2] <= 1 : 
                DP_checker[pos2] = 1 
if (sum(DP_checker) != DP_number) and (sum(DP_checker)!=0) : 
    not_one_mile_DP_DP_distance  = [[0 for x in range(DP_number)] for y in range(DP_number)]
    for pos1, val1 in enumerate(DP_checker) : 
        for pos2, val2 in enumerate(DP_checker):
            not_one_mile_DP_DP_distance[pos1][pos2] = original_DP_DP_distance[pos1][pos2]
            not_one_mile_DP_DP_distance[pos2][pos1] = origianl_DP_DP_distance[pos2][pos1]
    [max_distance, max_distance_location] = max_distance_finder(not_one_mile_DP_DP_distance)
    
    count = 0 # count : a variable that counts how many times the program goes through while loop below
    # while loop below is same as while loop above. 
    # Only difference is that in step 5, change first_fixed_PL[1](which is distance from first_fixed_PL to first_DP) to 1
    # and change second_fixed_PL[1](which is distance from second_fixed_PL to second_DP) to 1
    while max_distance != 0 :  
        count = count + 1
        print("===========================================================================")
        print("LOOP "+str(count))
        print("current maximum distance = " + str(max_distance))
        first_DP = max_distance_location[0] # first_DP : DP number of first DP that creates the farthest distance
        second_DP = max_distance_location[1] # second_DP : DP number of second DP that creates the farthest distance
        print("and corresponding DP locations = " + str(first_DP)+ " & " + str(second_DP)) 
        first_coordinates = DP_pos[first_DP] # [latitude, longitude] of first_DP
        second_coordinates = DP_pos[second_DP] # [latitude, longitude] of second_DP
        # comparing latitude of first_DP and second_DP / if second one is bigger, which_lat_bigger = "s", if not, which_lat_bigger = "f"
        if first_coordinates[0] <= second_coordinates[0] : which_lat_bigger = "s"
        else : which_lat_bigger = "f"
        # comparing longitude of first_DP and second_DP / if second one is bigger, which_long_bigger = "s", if not, which_long_bigger = "f"
        if first_coordinates[1] <= second_coordinates[1] : which_long_bigger = "s"
        else : which_long_bigger = "f"

    ## Create ordered list of PLs near first_DP and second_DP (based on which_lat_bigger, which long bigger)
        if (which_lat_bigger == "s") and (which_long_bigger =="f"):
            [PLs_near_first_DP, PLs_near_second_DP] = lat_bigger_s_long_bigger_f()
        elif (which_lat_bigger == "s") and (which_long_bigger == "s") : 
            [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_s_long_bigger_s()
        elif (which_lat_bigger == "f") and (which_long_bigger == "s") : 
            [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_f_long_bigger_s()
        elif (which_lat_bigger == "f") and (which_long_bigger == "f") : 
            [PLs_near_first_DP, PLs_near_second_DP] =lat_bigger_f_long_bigger_f()

    ### STEP 3 : Fix two PLs by calculating time
        # first_fixed_PL : (PL number of PL that makes path from first_DP to second_DP less than 45 minutes, distance from this PL to first_DP)
        # second_fixed_PL : (PL_number of PL that makes path from first_DP to second_DP less than 45 minutes, distance from this PL to second_DP)
        [first_fixed_PL, second_fixed_PL] = get_fixed_points(PLs_near_first_DP, PLs_near_second_DP) 
        print("=====TWO PLs FIXED=====")
        print("Fixed First PL : " + str(first_fixed_PL) + " / Fixed Second PL : " + str(second_fixed_PL))
        # set DP_DP_distance of first_DP and second_DP to 0 since we finished considering that case
        not_one_mile_DP_DP_distance[first_DP][second_DP] = 0 
        not_one_mile_DP_DP_distance[second_DP][first_DP] = 0 

    ### STEP 4 : Make lists of PLs that are within 0.25 miles from first_fixed_PL and second_fixed_PL 
    ## When both that element and PL1/PL2 are not special PLs, change that element’s value in PL_vector to -1.
    ## (-1 means that that PL is no longer possible to have bike station)
    ## Change first_fixed_PL and second_fixed_PL's PL_vector to 1. 
        PLs_near_first_PL = [] # all PLs(including first_fixed_PL) that are inside 0.25 radius with center of first_fixed_PL 
        for index, value in enumerate(PL_PL_distance[first_fixed_PL[0]]) : 
            if value <= 0.25 : PLs_near_first_PL = PLs_near_first_PL + [(index,value)]
        print("All PLs near first fixed PL : "+ str(PLs_near_first_PL))
        for pos, val in PLs_near_first_PL : # going through each element in PLs_near_first_PL
            if pos != first_fixed_PL[0] :
                if PL_extra[pos][1] == 0 and PL_extra[first_fixed_PL[0]][0] == 0 : 
                    PL_vector[pos]= -1 # change element of PL_vector to -1, when at least one of first_fixed_PL and another PL is not special
            else : PL_vector[first_fixed_PL[0]] = 1 # set element of PL_vector to 1 if corresponding PL is fixed
        
        PLs_near_second_PL = [] # all PLs(including second_fixed_PL) that are inside 0.25 radius with center of second_fixed_PL 
        for index, value in enumerate(PL_PL_distance[second_fixed_PL[0]]) : 
            if value <= 0.25 : PLs_near_second_PL = PLs_near_second_PL + [(index,value)]
        print("All PLs near second fixed PL : "+ str(PLs_near_second_PL))
        for pos, val in PLs_near_second_PL : # going through each element in PLs_near_second_PL
            if pos != second_fixed_PL[0] :
                if PL_extra[pos][1] == 0 and PL_extra[second_fixed_PL[0]][0] == 0 : 
                    PL_vector[pos]= -1 # change element of PL_vector to -1, when at least oen of second_fixed_PL and another PL is not special
            else : PL_vector[second_fixed_PL[0]] = 1  # set element of PL_vector to 1 if corresponding PL is fixed
        
        print("\nupdated PL_vector : "+str(PL_vector))

    ### STEP 5 : Remove cases of DPs that are near fixed PLs that are within 1 mile from first_fixed_PL and 1 mile from second_fixed_PL. 
    ### Then, since combinations of DPs in those lists are reachable within 45 minutes, change those cases' DP_DP_distance to 0. 
        DPs_near_first_fixed_PL = [] # list of all DPs that are inside radius of (distance between first_DP and first_fixed_PL) with first_fixed_PL as a center
        for pos, val in enumerate(PL_DP_distance[first_fixed_PL[0]]) :
    ## IMPORTANT : ONLY DIFFERENCE IS CHANGING FROM first_fixed_PL[1](which is distance from first_fixed_PL to first_DP) TO 1
            if val <= 1 : DPs_near_first_fixed_PL = DPs_near_first_fixed_PL + [(pos,val)]
        print("excluded DPs that are near first DP : " +str(DPs_near_first_fixed_PL)) 
        
        DPs_near_second_fixed_PL = [] # list of all DPs that are inside radius of (distance between second_DP and second_fixed_PL) with second_fixed_PL as a center
        for pos, val in enumerate(PL_DP_distance[second_fixed_PL[0]]) :
    ## IMPORTANT : ONLY DIFFERENCE IS CHANGING FROM second_fixed_PL[1](which is distance from second_fixed_PL to second_DP) TO 1
            if val <= 1 : DPs_near_second_fixed_PL = DPs_near_second_fixed_PL + [(pos,val)]
        print("excluded DPs that are near second DP : " +str(DPs_near_second_fixed_PL))
        
        # go through all possible combinations of DPs_near_first_fixed_PL and DPs_near_second_fixed_PL and change corresponding DP_DP_distance to 0
        for pos, val in enumerate(DPs_near_first_fixed_PL) : 
            for pos1, val1 in enumerate(DPs_near_second_fixed_PL) : 
                not_one_mile_DP_DP_distance[val[0]][val1[0]]=0
                not_one_mile_DP_DP_distance[val1[0]][val[0]]=0
        print("end of loop number "  + str(count)+"\n\n")
    ### STEP 6 : Find two DPS that are farthest apart. 
    ## if max_distance is not equal to 0, while loop will run again / if not, move on to Part 2
        [max_distance, max_distance_location] = max_distance_finder(not_one_mile_DP_DP_distance) 
    
############### Part 1 ENDS HERE ###############
    ############### PRINTING OUT RESULTS FROM Part 1 ############### 
    print("PL_vector after Part 1 : " +str(PL_vector))
    ## MUN_count : number of bike stations fixed from Algorithm 1 for each municipality
    MUN_count = [0 for x in range(MUN_number)]
    for pos, val in enumerate(PL_vector) : 
        if val == 1 : MUN_count[int(PL_extra[pos][0])] = MUN_count[int(PL_extra[pos][0])] + 1
    print("Number of bike stations fixed from Part 1 for each municipality : " + str(MUN_count))


############### PART 2 STARTS HERE ###############
############### FUNICTION LIST for Part 2 ###############

# Count the number of stations
def station_counter(mun, PL_vector, PL_extra):
    st = 0;
    for i in range(len(PL_vector)):
        if (PL_vector[i] == 1) & (PL_extra[i][0] == mun):
            st = st + 1
    return st

# Add n stations in the called municipality by mutating the stations' marked value 0 to 1 in PL_vector;
# Throw exception if it is impossible to add n more new stations in the municiplaity
def add_s_station(n, PL_vector, mun, PL_extra):

    count = n
    temporary_PL_vector = PL_vector
    # This loop runs until all the n stations are added, temporary_PL_vector will be changed accordingly
    # It will throw exception if it is impossible to add n new stations
    while (count != 0):
        affect_counter_vector = []
        min_affect= len(temporary_PL_vector)
        # This loop goes through all the current potential PLs (0s) in temporary_PL_vector to record for each of them,
        # how many numbers of other potential PLs are affected because of the 0.25 mile distance constraint.
        # affect_counter_vector records down these numbers with the corresponding PL number - (PL number, how many affected)
        for i in range(len(PL_extra)):
            if (PL_extra[i][0] == float(mun)) & (temporary_PL_vector[i] == 0):
                affect_counter = 0
                # This loop go through each PL location to see how many locations will no longer be a potential PL because of setting station at PLi
                for index, value in enumerate(PL_PL_distance[i]) : 
                    if (value <= 0.25) & (value > 0.0) & (PL_extra[i][1] == 0) & (PL_extra[index][1] == 0) : affect_counter = affect_counter + 1
                affect_counter_vector = affect_counter_vector + [(i, affect_counter)]
                if min_affect > affect_counter:
                    # min_affect records down the minimum affected number of PL locations that can no longer be potential PL locations
                    min_affect = affect_counter

        # If there is no potential PL, affect_counter_vector will be empty, so exception will be thrown. Adding n stations fails.
        if affect_counter_vector == []:
            raise Exception

        # Change the potential PL that affects the least number of other potential PLs from 0 to 1 (no station to small station)
        for pos, affect_count in affect_counter_vector:
            if affect_count == min_affect:
                temporary_PL_vector[pos] = 1
                for index, value in enumerate(PL_PL_distance[pos]): 
                    if (value <= 0.25) & (value > 0.0) & (PL_extra[pos][1] == 0) & (PL_extra[index][1] == 0): 
                        temporary_PL_vector[index] = -1;
                count = count - 1
                break

    # temporary_PL_vector is the final PL_vector after adding n new stations, since adding n stations succeeds, update the global PL_vector accordingly
    PL_vector = temporary_PL_vector
    st[mun] = st[mun] + n

# Find how many stations should be small, medium and large and return these three numbers
def s_m_l_solver(mun, PL_vector, PL_extra, MUN_minmax):
    D_min = MUN_minmax[mun][0]
    D_max = MUN_minmax[mun][1]

    # Case when the current bikes held by small stations already satisfies the bike number requirement of the municipality
    if (10 * st[mun] >= D_min) & (10 * st[mun] <= D_max):
        s = st[mun]
        m = 0
        l = 0
        return s, m, l

    # Case when the current bikes held by small stations already surpasses the bike number requirement of the municipality
    elif 10 * st[mun] > D_max:
        raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too small maximum bike number requirements to handle")

    # Case when the current number of bikes held by small stations is not enough, but it is totally possible to meet the requirement by adjusting the station size  
    if (10 * st[mun] < D_min) & (50 * st[mun] >= D_min):
        d = D_min - 10 * st[mun];
        k = d // 10;

        # see whether changing all curent stations to medium is enough (one more medium station change from small increases bike numbers by 10, which is the smallest indentation we can manipulate)
        if k <= st[mun]:
            # small, medium, large station numbers when it is enough to just change small station to medium
            m = k
            l = 0
            s = st[mun] - k
            return s, m, l

        else:
            # when it is not enough to just change small station to medium
            # Calculate how many bikes are still lacked after changing all to medium and get optimal solution for each case
            dd = D_min - 20 * st[mun]
            # Calculate how many medium station should be changed to large
            kk = dd // 30
            # Calculate how many bikes are still lacked after changing some medium station to large
            rr = dd % 30;

            # 0 bike is lacked, return corresponding small, medium, large station numbers
            if rr == 0:
                l = kk
                s = 0
                m = st[mun] - l - s
                return s, m, l

            # if 1-10 are lacked, and there is a large station
            elif (rr > 0) & (rr <= 10) & (kk != 0):
                # try whether it is possible to add two more stations because 3 medium is better than 1 large, 1 small
                try:
                    add_s_station(2, PL_vector, mun, PL_extra)
                except Exception:
                    # adding 2 fails
                    # try whether it is possible to add 1 more station
                    try:
                        add_s_station(1, PL_vector, mun, PL_extra)
                    except Exception:
                        # adding 1 fails
                        # if there are >= 3 medium stations, change 1 medium to large, 2 medium to small (optimal)
                        if kk <= st[mun] - 3:
                            l = kk + 1
                            s = 2
                            m = st[mun] - l - s
                            return s, m, l

                        # if there are 2 medium stations, change 1 medium to large, 1 medium to small (optimal)
                        elif kk == st[mun] - 2:
                            l = kk + 1
                            s = 1
                            m = st[mun] - l - s
                            return s, m, l

                        # if there is 1 medium station, change 1 medium to large (optimal)
                        elif kk == st[mun] - 1:
                            l = kk + 1
                            s = 0
                            m = st[mun] - l - s
                            return s, m, l
                        # It is not possible all of them are already large because of former contraint, if all current stations are large, it must already be enough

                    # Adding one station succeeds, then adding one small is optimal
                    l = kk
                    s = 1
                    m = st[mun] - l - s
                    return s, m, l
                # Adding two station succeeds, then adding two medium, change 1 large to medium is optimal because 3 medium is better than 1 large 1 small
                l = kk - 1
                s = 0
                m = st[mun] - l - s
                return s, m, l

            # if 1-10 are lacked, and there is no large station
            elif (rr > 0) & (rr <= 10) & (kk == 0):
                #try add 1 new station
                try:
                    add_s_station(1, PL_vector, mun, PL_extra)
                except Exception:
                    #adding 1 station fails, then only way is changing one medium to large
                    l = 1
                    s = 0
                    m = st[mun] - l - s
                    return s, m, l
                #adding 1 succeeds, then we need one more small station, others are medium
                l = 0
                s = 1
                m = st[mun] - l - s
                return s, m, l

            # if 11-20 are lacked, but there is no large station
            elif (rr > 10) & (rr <= 20):
                #try add 1 new station
                try:
                    add_s_station(1, PL_vector, mun, PL_extra)
                except Exception:
                    # adding 1 station fails
                    # if there are >= 2 medium stations, change 1 medium to large, 1 medium to small (optimal)
                    if kk <= st[mun] - 2:
                        l = kk + 1
                        s = 1
                        m = st[mun] - l - s
                        return s, m, l

                    # if there is only 1 medium station, change 1 medium to large(optimal)
                    if kk == st[mun] - 1:
                        l = kk + 1
                        s = 0
                        m = st[mun] - l - s
                        return s, m, l
                    # It is not possible all of them are already large because of former contraint, if all current stations are large, it must already be enough
                # Adding one station succeeds, then adding one medium is optimal
                l = kk
                s = 0
                m = st[mun] - l - s
                return s, m, l

            #if 21-30 are lacked, just change one medium to large
            elif (rr > 20) & (rr < 30):
                l = kk + 1
                s = 0
                m = st[mun] - l - s
                return s, m, l

    # Case when current number of stations can not meet minimum requirement even all of them are changed to large stations
    elif 50 * st[mun] < D_min:
        # Calculate how many bikes are still lacked after changing all to large and get optimal solution for each case, there may be no solution.
        D = D_min - 50 * st[mun]
        # Calculate how many new large stations to add - 2p is the number of large stations to add here
        p = D // 100
        # Calculate how many still lacks after adding 2p large stations
        d = D % 100

        #try to add 2p new stations
        try:
            add_s_station(p * 2, PL_vector, mun, PL_extra)
        #addung fails, this means it is impossible to reach a feasible solution
        except Exception: raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")

        # Adding 2p large stations succeeds
        # 0 bike lacked so optimal solution is make stations all large stations
        if (d == 0):
            m = 0
            s = 0
            l = st[mun] - m - s

        # following 10 cases give analysis for 1-10, 11-20 ...... 91-99 bike lacked and calculate for an optimal solution 
        # or throw exception to say this program fails to solve the problem
        elif (d != 0) & (d <= 10):
            try:
                add_s_station(1, PL_vector, mun, PL_extra)
            except Exception:
                raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
            m = 0
            s = 1
            l = st[mun] - m - s
            return s, m, l

        elif d <= 20:
            try:
                add_s_station(1, PL_vector, mun, PL_extra)
            except Exception:
                raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
            m = 1
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 30:
            try:
                add_s_station(2, PL_vector, mun, PL_extra)
            except Exception:
                try:
                    add_s_station(1, PL_vector, mun, PL_extra)
                except Exception:
                    raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
                m = 0
                s = 0
                l = st[mun] - m - s
                return s, m, l
            m = 1
            s = 1
            l = st[mun] - m - s
            return s, m, l

        elif d <= 40:
            try:
                add_s_station(2, PL_vector, mun, PL_extra)
            except Exception:
                try:
                    add_s_station(1, PL_vector, mun, PL_extra)

                except Exception:
                    raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
                m = 0
                s = 0
                l = st[mun] - m - s
                return s, m, l
            m = 2
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 50:
            try:
                add_s_station(1, PL_vector, mun, PL_extra)
            except Exception:
                raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
            m = 0
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 60:
            try:
                add_s_station(3, PL_vector, mun, PL_extra)
            except Exception:
                try:
                    add_s_station(2, PL_vector, mun, PL_extra)
                except Exception:
                    raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
                m = 0
                s = 1
                l = st[mun] - m - s
                return s, m, l
            m = 3
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 70:
            try:
                add_s_station(2, PL_vector, mun, PL_extra)
            except Exception:
                raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
            m = 1
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 80:
            try:
                add_s_station(4, PL_vector, mun, PL_extra)
            except Exception:
                try:
                    add_s_station(3, PL_vector, mun, PL_extra)
                except Exception:
                    try:
                        add_s_station(2, PL_vector, mun, PL_extra)
                    except Exception:
                        raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
                    m = 0
                    s = 0
                    l = st[mun] - m - s
                    return s, m, l
                m = 1
                s = 1
                l = st[mun] - m - s
                return s, m, l
            m = 4
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d <= 90:
            try:
                add_s_station(3, PL_vector, mun, PL_extra)
            except Exception:
                try:
                    add_s_station(2, PL_vector, mun, PL_extra)
                except Exception:
                    raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
                m = 0
                s = 0
                l = st[mun] - m - s
                return s, m, l
            m = 2
            s = 0
            l = st[mun] - m - s
            return s, m, l

        elif d < 100:
            try:
                add_s_station(2, PL_vector, mun, PL_extra)
            except Exception:
                raise Exception("This solution program fails to solve this project because municipality" + str(mun) + "has too large munimum bike number requirements to handle")
            m = 0
            s = 0
            l = st[mun] - m - s
            return s, m, l


# Adjust PL_vector, -1 - impossible location, 0 - no station but possible adding location, 1 - small station, 2 - medium station, 3 - large station
def PL_vector_adjuster(mun, PL_vector, PL_extra, MUN_minmax):

    s, m, l = s_m_l_solver(mun, PL_vector, PL_extra, MUN_minmax)
    print("Municipality " + str(mun) + " should have " + str(s) + " small stations, " + str(m) + " medium stations and " + str(l) + " large stations.")
    count_m = m
    count_l = l
    for i in range(len(PL_vector)):
        if (PL_extra[i][0] == mun) & (PL_vector[i] == 1):
            if count_m != 0:
                PL_vector[i] = 2
                count_m = count_m - 1
            elif count_l != 0:
                PL_vector[i] = 3
                count_l = count_l - 1
            else:
                break
    return


# Calculate cost of the project based on the optimal station plan and print it out
def cost_calclator (PL_vector):

    cost = 0
    for i in range(len(PL_vector)):
        if PL_vector[i] == 1:
            cost = cost + 5000

        elif PL_vector[i] == 2:
            cost = cost + 8000

        elif PL_vector[i] == 3:
            cost = cost + 20000
    print("Total cost of building all stations is: ")
    print(cost)
    return
############### Function List of Part 2 Ends ###############

### STEP 1 : Count how many set stations are there in each municipality according to the plan before meeting the bike number requirement of each municipality.
st = []

for i in range(MUN_number):
    st.append(station_counter(i, PL_vector, PL_extra))

### STEP 2 : Calculate the number of small, medium and large stations needed for each municipal 
### STEP 3 : Adjust the PL_vector to meet the bike number requirement of each municipality
for i in range(MUN_number):
    PL_vector_adjuster(i, PL_vector, PL_extra, MUN_minmax)

print("PL_vector after considering station size and municipality bike numbers is: ")
print(PL_vector)

### STEP 4: Calculate the total station setting cost of this optimal plan
cost_calclator (PL_vector)
############### PART 2 ENDS HERE ###############

############### CREATING TXT FILES ###############
## setting up name for output file 
keyword = input("What do you want to have for your name of your output file? ")

file = open("sol_"+keyword+".txt","w")
file.write("Station Size\n")
for pos, val in enumerate(PL_vector) : 
    if val != -1 and val != 0 : 
        file.write("p"+str(pos)+" "+str(val)+"\n")
file.close()
print("check your folder to find sol_"+keyword+".txt file")
############### PLOTTING ON GOOGLE MAP ###############
## finding average of latitude and average of longitude to find part of the world to show on Google Map
for pos, val in enumerate(DP_pos) : 
    if pos == 0 : lat_min, lat_max, long_min, long_max = val[0], val[0], val[1], val[1]
    else : 
        if val[0] <= lat_min : lat_min = val[0]
        elif val[0] >= lat_max : lat_max = val[0]
        if val[1] <= long_min : long_min = val[1]
        elif val[1] >= lat_max : long_max = val[1]  
lat_average = (lat_min+lat_max)/2
long_average = (long_min+long_max)/2 
gmap = gmplot.GoogleMapPlotter(lat_average, long_average, 13)
## Organizing and plotting DP points that should be shown on Google Map (Blue dots)
DP_gmplot = [] 
for pos, val in enumerate(DP_pos) : 
    lat, lon = val[0], val[1]
    DP_gmplot = DP_gmplot +[(lat,lon)]
DP_gmplot_lat, DP_gmplot_lon = zip(*DP_gmplot)
gmap.scatter(DP_gmplot_lat, DP_gmplot_lon, '#0000FF', size=100, marker=False)
## Organizing and plotting PL points that should be shown on Google Map 
# 1) small PLs = red dots 
final_points_small = []
for pos, val in enumerate(PL_vector) : 
    if val == 1 : 
        lat, lon = PL_pos[pos][0], PL_pos[pos][1]
        final_points_small = final_points_small  + [(lat,lon)]
if len(final_points_small) != 0 : 
    final_points_small_lat, final_points_small_lon = zip(*final_points_small)
    gmap.scatter(final_points_small_lat, final_points_small_lon, '#FF0000', size=100, marker=False)
# 2) medium PLs = black dots
final_points_medium = []
for pos, val in enumerate(PL_vector) : 
    if val == 2 : 
        lat, lon = PL_pos[pos][0], PL_pos[pos][1]
        final_points_medium = final_points_medium  + [(lat,lon)]
if len(final_points_medium) != 0 : 
    final_points_medium_lat, final_points_medium_lon = zip(*final_points_medium)
    gmap.scatter(final_points_medium_lat, final_points_medium_lon, '#000000', size=100, marker=False)
# 3) large PLs = cyan dots
final_points_large = []
for pos, val in enumerate(PL_vector) : 
    if val == 3 : 
        lat, lon = PL_pos[pos][0], PL_pos[pos][1]
        final_points_large = final_points_large  + [(lat,lon)]
if len(final_points_large) != 0 : 
    final_points_large_lat, final_points_large_lon = zip(*final_points_large)
    gmap.scatter(final_points_large_lat, final_points_large_lon, '#00CCFF', size=100, marker=False)

## Saving Google Map link as html file
gmap.draw(keyword+".html")
print("check your folder to find "+keyword+".html for google map\n")

print("END OF PROGRAM FOR PHASE 1")
#####  END OF PROGRAM FOR PHASE 1 ##### 