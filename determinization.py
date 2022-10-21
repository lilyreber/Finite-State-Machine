from collections import deque
from parser_fsm import read_fsm
from parser_fsm import FSM 
from parser_fsm import fsm_global
import copy
import sys


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
    res.initial_state = str(set(inp.initial_state))
    return res


def main():
    fsm1 = copy.deepcopy(read_fsm(sys.argv[1]))
    wfile = open(sys.argv[1] + ".out", 'w')
    wfile.write(determine(fsm1).print())
if __name__ == "__main__":
    main()
