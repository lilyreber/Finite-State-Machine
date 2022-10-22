from ast import operator
from collections import deque
from os import rename
from platform import mac_ver
from parser_fsm import read_fsm
from parser_fsm import FSM 
from parser_fsm import fsm_global
import copy
import sys
import re


def make_good_names(machine):
    class mydict:
        d = dict()
        i=0
        def __getitem__(self, ky):
            if ky not in self.d:
                self.i+=1
                self.d[ky] = str(self.i)
            return self.d[ky]
    renamer = mydict()

    states = set()
    for s in machine.states:
        states.add(renamer[s])
    machine.states = states

    machine.initial_state = renamer[machine.initial_state]

    finite_states = set()
    for s in machine.finite_states:
        finite_states.add(renamer[s])
    machine.finite_states = finite_states

    transition = dict()
    for t in machine.transition.keys():
        transition[(renamer[t[0]], t[1])] = set()
        for p in machine.transition[t]:
            (transition[(renamer[t[0]], t[1])]).add(renamer[p])
    machine.transition = transition

    return machine



def print_fsm(machine):
    s = ""
    s+="STATES = "+str(machine.states).replace('\'', '').replace('\"', '').replace(' ', '')+"\n"
    s+="ALPHABET = "+str(machine.input_alphabet).replace('\'', '').replace('\"', '').replace(' ', '')+"\n"
    s+="INITIAL = {"+machine.initial_state+"}\n"
    s+="FINITE = "+str(machine.finite_states).replace('\'', '').replace('\"', '').replace(' ', '')+"\n"
    for x in machine.transition:
            for y in machine.transition[x]:
                s+=f"({x[0]}) ++ \"{x[1]}\" -> ({y})"+"\n"
    return s
    
        
def check_determinism(machine):
    for key in machine.keys():
        if len(set(machine[key])) >1:
            return False
    return True

def determine(inp):
    q = deque()
    oldq = deque()
    s = set()
    s.add(inp.initial_state)
    q.appendleft(s)
    res_finite_states = set()
    res_states = set()
    initstate = set()
    initstate.add(inp.initial_state)
    res_states.add(frozenset(initstate))
    if inp.initial_state in inp.finite_states:
        res_finite_states.add(frozenset(initstate))
    res_transition = dict()
    while (len(q)!=0):
        s = q.pop()
        oldq.append(s)
        for cc in inp.input_alphabet:
            set_of_states = set()
            for from_state in s:
                if (from_state, cc) in inp.transition:
                    set_of_states = set_of_states | inp.transition[(from_state, cc)]
            if (set_of_states not in q) and ((set_of_states not in oldq)) and set_of_states!=set():
                q.appendleft(set_of_states)
            if set_of_states.intersection(inp.finite_states)!=set():
                res_finite_states.add(frozenset(set_of_states))
            if set_of_states!=set():
                res_states.add(frozenset(set_of_states))
                res_transition[frozenset(s), cc] = frozenset(set_of_states)
    fsm_global.clear()
    res = FSM()
    for state in res_finite_states:
        res.finite_states.add(str(set(state)))
    for state in res_states:
        res.states.add(str(set(state)))
    
    for key in res_transition.keys():
        s = str(set(res_transition[key]))
        if (str(set(key[0])), key[1]) not in res.transition:
            res.transition[(str(set(key[0])), key[1])] = set()
        (res.transition[(str(set(key[0])), key[1])]).add(s)
    res.input_alphabet = inp.input_alphabet
    initstateset = set()
    initstateset.add(str(inp.initial_state))
    res.initial_state = str(initstateset)
    res = make_good_names(res)
    return res


def main():
    fsm1 = copy.deepcopy(read_fsm(sys.argv[1]))
    #fsm1 = copy.deepcopy(read_fsm("example_for_determinization/bin.txt"))
    wfile = open(sys.argv[1] + ".out", 'w')
    wfile.write(print_fsm(determine(fsm1)))
if __name__ == "__main__":
    main()
