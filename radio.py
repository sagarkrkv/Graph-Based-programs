# B551 Fall 2015
# Vidya Sagar Kalvakunta (vkalvaku)
# radio.py
'''
Here we are supposed to assign frequencies to all the states that are in the adjacent-states file
such that no adjacent states have the same frequency.

In the prob statement it was given that
 avail_freq = ("A","B","C","D")

 First we read the adjacent-states file and store the states and their adjacent states in a dict 
 called adjacent_states. 
    adjacent_states = {
                        state:[adjacent_states]
                      }
I have designed it to handle even noisy data and add only non-duplicate data and data that is valid

I have created two dicts radio_assigned_list,radio_used_list
        radio_assigned_list = {
                                state:[frequency assigned]
                               }
        radio_used_list =   {
                                state:[frequencies assigned to its neighbour]
                            }

Then the program reads the constraints file given as argument and updates the values of 
the state in the radio_assigned_list and radio_used_list

The program has four important functions
1.) freq_assign()
2.) freq_ok()
3.) used_freq_assign()
4.) greatest()

FREQ_ASSIGN():
    This function recursively assigns frequency to all states, It takes a state as an input, 
    and checks the frequencies that are available to it

        using set(avail_freq) - set(radio_used_list[curr_state])

    then it assigns a frequency from that set and updates values of radio_assigned_list 
    and radio_used_list.
    then it calls the greatest() and it again calls itself using the state provided by the 
    greatest() as the current state

    If none of the frequencies can be assigned to a particular state, it returns false and 
    backtracks to the previous state

FREQ_OK():
    This function takes two parameters ,state and freq . It effectively checks if a given 
    freq is already assigned to any of its neighbours. It returns false if it fails the condition

USED_FREQ_ASSIGN():
    This Function takes a state as an input parameter updates the radio_used_list such that it 
    contains the list of freqs that cannot be used for all neighbours of that state.

GREATEST():
    Returns the state with the most number of constraints i.e the state which has the least 
    number of frequencies to choose from.

\


For each frequency we check if it satisfies the constraint, i.e it doesn't conflict 
with its neighbour,in the future ,i.e forward checking.

If this holds good, we assign the frequency to the state and choose the next state but if it
leads to any problem, then we choose another frequency from available frequency set. 
If all the frequencies have been checked, but still no frequency is good to be allocated,
then we backtrack to the previous state and change the allocated frequency of that state 
and again update all the neighbouring states with available frequencies. Once a frequency 
is allocated to a state we remove that frequency from the available frequency list of all the 
neighbours of that state.

This program gives backtrack as 0 for constraint-file-1 and constraint-file-2
 while giving backtrack 2 for constraint-file-3  

'''
import sys
import os


avail_freq = ("A","B","C","D")
backtrack_count = 0


def freq_ok(curr_state,freq):  ## Function to check if a given freq can be assigned to state i.e it checks if any of its neighbours have the same freq 
    for neighbour in adjacent_states[curr_state]:
        if freq == radio_assigned_list[neighbour]:
            return False
    return True

def used_freq_assign(curr_state): ## Function updates the list of freqs that cannot be used for all neighbours of the current state    
    for adj_state in adjacent_states[curr_state]:
        radio_used_list[adj_state] = []
        for neighbour in adjacent_states[adj_state]:
            if radio_assigned_list[neighbour] != 0 and radio_assigned_list[neighbour] not in radio_used_list[adj_state]:
                radio_used_list[adj_state].append(radio_assigned_list[neighbour])

def freq_assign(curr_state): #This function recursively assigns frequency to all states
    if 0 not in radio_assigned_list.values(): ## Returns true if all states are assigned values
        return True
    
    for freq in set(avail_freq) - set(radio_used_list[curr_state]):#
        if freq_ok(curr_state,freq):
            radio_assigned_list[curr_state] = freq
            used_freq_assign(curr_state)
            nextnode = greatest()
            if freq_assign(nextnode):
                return True
            else:
                radio_assigned_list[curr_state] = 0
                used_freq_assign(curr_state)
    
    global backtrack_count            
    backtrack_count += 1
    return False

def greatest(): ## Returns the state with the most number of constraints i.e the state which has the least number of frequencies to choose from
    beta = -100
    greatest = 0
    for tmp_state,adj in radio_used_list.items():
        if len(adj) > beta and radio_assigned_list[tmp_state] == 0:
                beta = len(adj)
                greatest = tmp_state             
    return greatest


def logic(): ## This function just calls the freq_assign Function
    curr_state = greatest()
    if freq_assign(curr_state):
        print "Number of backtracks: ",backtrack_count
        return True
    else:
        print "\nCannot assign frequency to states with the given constraints\n"

if __name__ == "__main__":
    adjacent_states = {}
    radio_assigned_list = {}
    radio_used_list = {}
    filename = sys.argv[1]
    
    with open('adjacent-states', 'r') as file: # reads adjacent-states file and stores the states and their adjacent states in a dict
                                               #it is designed to handle even noisy data            
        for line in file:
        	data = line.split()
        #   adjacent_states[data.pop(0)] = data    ### very fast implementation if given non noisy data 
        	initial = data.pop(0)
        	adjacent_states[initial] = (adjacent_states[initial] if initial in adjacent_states  else [])
        	for i in data:
                    if i not in adjacent_states[initial]: adjacent_states[initial].append(i)
                    adjacent_states[i] = (adjacent_states[i] if i in adjacent_states  else []) 
                    if initial not in adjacent_states[i]: adjacent_states[i].append(initial)
    
    for key,value in adjacent_states.items():# Adds all available states to dict radio_assgned_list and radio_used_list
    	radio_assigned_list[key] = 0
        radio_used_list[key] = []
    
    with open(filename, 'r') as file: #reads the constraints file given as argument and updates the values of the state 
                                      #in the radio_assigned_list and radio_used_list
        for line in file:
            tmp = line.split()
            if(len(tmp) == 2):
                state , value = tmp
                if state in radio_assigned_list: 
                    radio_assigned_list[state] = value
                    used_freq_assign(state)
  
    if logic(): # if the logic function returns true i.e if it is possible to assign freq to all states, it writes input in results.txt
        with open('results.txt', 'w' ) as writefile:
            for key,value in radio_assigned_list.items():
                writefile.write(key+" "+value+"\n")
            writefile.write("Number of backtracks: " + str(backtrack_count)) #prints no of backtracks in last line of the file



   