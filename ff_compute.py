import sys

###
 # Reading in the grammar file
###
if len(sys.argv) != 3:
    print("---- BAD ARGS ----")
    exit(1)
else:
    g = open(sys.argv[1], "r")
    ff = open(sys.argv[2], "w")
    production = g.readline()

# g = open("input3.txt", "r")
# ff = open("myoutput.txt", "w")
# production = g.readline()

productions = []
nonterminals = []


###
 # Creating a list of tuples to store the productions
###
while production:
    production = production.split("->")
    production[0] = production[0].strip()
    production[1] = production[1].strip()
    productions.append((production[0], production[1]))
    production = g.readline()


###
 # Creating a list of the non-terminals to compute the FIRST and FOLLOW sets for
###
for p in productions:
    if p[0] not in nonterminals:
        nonterminals.append(p[0])

###
 # canDeriveEpsilon(non_t) checks if a non-terminal can derive epsilon
 # Returns True if the non-terminal can derive epsilon, otherwise it returns False
###
def canDeriveEpsilon(non_t):
    for production in productions:
        if production[0] == non_t:
            if production[1] == "":
                return True

###
 # FIRST(elem) computes the FIRST set of a non-terminal 
 # Returns the FIRST set of non_t
###
FIRST_sets = {}
def FIRST(non_t, first, cde):
    
    caller_first = first
    first = []
    
    # check if non-terminal can derive epsilon before computing FIRST set
    if canDeriveEpsilon(non_t):
        cde = True
        if "" not in first:
            first.append("")
    
    for production in productions:
        
        if production[0] == non_t: # if lhs == non-terminal
            
            rhs = list(production[1])
            for i in range(len(rhs)): # go through every symbol in the rhs
                
                if rhs[i] == " ":
                    continue # skip whitespace
                
                if rhs[i] == "$":
                    first.append("$$")
                    break # move to next production
                
                if rhs[i].islower() or rhs[i] == "": # if first character of elem is a terminal or epsilon
                    if rhs[i] not in first:
                        first.append(rhs[i])
                        break # move to next production
                        
                else: # if first character of elem is a non-terminal
                    if rhs[i] == non_t: # ensure non_t does not call FIRST on itself
                        if non_t in FIRST_sets.keys():
                            if FIRST_sets[non_t][1]: # if non_t derives epsilon or is empty
                                continue # keep searching rhs for a terminal                        
                        else: # non_t not in FIRST_sets; FIRST(non_t) has not been computed
                            if cde:
                                continue # keep searching rhs for a terminal
                        break  # move to next production
                    if FIRST(rhs[i], first, cde)[1]: # if non-terminal can derive epsilon
                        cde = True
                    else:
                        break # move to next production
                        
    # recursively adding non-terminal to FIRST_sets while computing the calling non-terminal's FIRST set
    if non_t not in FIRST_sets.keys(): 
        FIRST_sets[non_t] = first  
    
    # merge the calling non-terminal's FIRST set with the FIRST set of the non-terminal
    for t in first:
        if t not in caller_first:
            caller_first.append(t)        
    return (caller_first, cde)
    

###
 # FOLLOW(elem) computes the FOLLOW set of a non-terminal 
 # Returns the FOLLOW set of non_t
###
FOLLOW_sets = {"S'": [""]}
def FOLLOW(non_t, follow):
    
    caller_follow = follow
    follow = []
    
    for production in productions:
        
        if non_t in production[1]:
                
            if non_t == production[1][-1]: # if non_t is the last symbol in the rhs
                if production[0] == non_t:
                    continue
                FOLLOW(production[0], follow)
                
            else: # if non_t is not the last symbol in the rhs
                symbolAfter = production[1][production[1].index(non_t)+1:].lstrip()[0]
                
                if symbolAfter.islower(): # symbol after non_t is a terminal
                    follow.append(symbolAfter)
                else: # symbol after non_t is a non-terminal
                    if symbolAfter == "$":
                        follow.append("$$")
                        continue
                    if "" in FIRST_sets[symbolAfter]: # if the symbol after can derive epsilon
                        FOLLOW(symbolAfter, follow) # FOLLOW(non_t) U FIRST(symbolAfter)
                    for t in FIRST_sets[symbolAfter]: # add all terminals in FIRST(symbolAfter) to FOLLOW(non_t)
                        if t not in follow:
                            follow.append(t)
                            
    # recursively adding non-terminal to FOLLOW_sets while computing the calling non-terminal's FOLLOW set
    if non_t not in FOLLOW_sets.keys(): 
        FOLLOW_sets[non_t] = follow  
    
    # merge the calling non-terminal's FOLLOW set with the FOLLOW set of the non-terminal
    for t in FOLLOW_sets[non_t]:
        if t not in caller_follow:
            caller_follow.append(t)
    return caller_follow


###
 # Computing the first and follow sets for each non-terminal
###
for nt in nonterminals:
    if nt not in FIRST_sets.keys():
        FIRST_sets[nt] = FIRST(nt, [], False)[0]

for nt in nonterminals:
    if nt not in FOLLOW_sets.keys():
        FOLLOW_sets[nt] = FOLLOW(nt, [])


###
 # Printing the non-terminals and their associated FIRST and FOLLOW sets
###
nonterminals.sort()
nonterminals.remove("S'")
nonterminals.insert(0, "S'")

for nt in nonterminals:
    
    # Order the FIRST sets
    FIRST_sets[nt].sort()
    if "$$" in FIRST_sets[nt]:
        FIRST_sets[nt].remove("$$")
        FIRST_sets[nt].append("$$")
    if "" in FIRST_sets[nt]:
        if len(FIRST_sets[nt]) > 1:
            FIRST_sets[nt].remove("")
        
    # Order the FOLLOW sets
    FOLLOW_sets[nt].sort()
    if "$$" in FOLLOW_sets[nt]:
        FOLLOW_sets[nt].remove("$$")
        FOLLOW_sets[nt].append("$$")
    if "" in FOLLOW_sets[nt]:
        if len(FOLLOW_sets[nt]) > 1:
            FOLLOW_sets[nt].remove("")
    
    # Write the non-terminal
    ff.write(nt+"\n")
    # Write the FIRST set
    for terminal in FIRST_sets[nt]:
        ff.write(terminal + "\n") if terminal == FIRST_sets[nt][-1] else ff.write(terminal + ", ")
    # Write the FOLLOW set
    for terminal in FOLLOW_sets[nt]:
        if nt != nonterminals[-1]:
            ff.write(terminal + "\n") if terminal == FOLLOW_sets[nt][-1] else ff.write(terminal + ", ")
        else:
            ff.write(terminal) if terminal == FOLLOW_sets[nt][-1] else ff.write(terminal + ", ")


g.close()
ff.close()