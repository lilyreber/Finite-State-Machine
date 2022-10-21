from collections import deque
from parser_fsm import read_fsm
from parser_fsm import FSM 
from parser_fsm import fsm_global
import copy
import sys

def make_full(machine):
    devil_vertex = 'devil'
    for s in machine.states:
        devil_vertex+=s
    full = True
    for vertex in machine.states:
        for s in machine.input_alphabet:
            if (vertex, s) not in machine.transition:
                full= False
                machine.transition[(vertex, s)] = set()
                (machine.transition[(vertex, s)]).add(devil_vertex)
    if not full:
        machine.states.add(devil_vertex)
        for s in machine.input_alphabet:
            machine.transition[(devil_vertex, s)] = set()
            (machine.transition[(devil_vertex, s)]).add(devil_vertex)
    return machine


def minimize(machine):
    q=deque()
    d=dict()
    reverse_transitions = dict()
    for st in machine.states:
        for t in machine.input_alphabet:
            reverse_transitions[(st, t)] = set()
    for t in machine.transition:
        el = machine.transition[t].pop()
        machine.transition[t].add(el)
        (reverse_transitions[(el, t[1])]).add(t[0])
    for a in machine.states:
        for b in machine.states:
            d[(a,b)] = 0
    non_finite_state =machine.states - machine.finite_states
    for u in machine.finite_states:
        for v in non_finite_state:
            d[(u,v)] = 1
            d[(v,u)] = 1
            q.appendleft ((u,v))
            q.appendleft ((v,u))
    while len(q):
        (x,y) = q.pop()
        for c in machine.input_alphabet:
            for a in reverse_transitions[(x,c)]:
                for b in reverse_transitions[(y,c)]:
                    if d[(a,b)] == 0:
                        d[(a,b)] = 1
                        d[(b,a)] = 1
                        q.appendleft((a,b))
                    
    equivalent_vertexes = dict()
    for v in machine.states:
        equivalent_vertexes[v]=set()
        equivalent_vertexes[v].add(v)
    for v1 in machine.states:
        for v2 in machine.states:
            if d[(v1, v2)] ==0:
                equivalent_vertexes[v1].add(v2)
    ########## check that the automaton is already minimal
    already_min = True
    for v in machine.states:
        if len(equivalent_vertexes[v]) !=1:
            already_min = False
    if already_min:
        return machine
    ##########
    i=0
    init_class =0
    processed_vertexes = set()
    class_by_vertex=dict()
    vertexes_by_class = dict()
    for representative in machine.states:
        if representative not in processed_vertexes:
            i+=1
            vertexes_by_class[i]=set()
        for el in equivalent_vertexes[representative]:
            processed_vertexes.add(el)
            class_by_vertex[el] = i
            vertexes_by_class[i].add(el)
    res = FSM()
    res.finite_states=set()
    res.initial_state=None
    res.input_alphabet=set()
    res.states=set()
    res.transition=dict()
    for c in range(1, i+1):
        res.states.add(str(c))
        for v in vertexes_by_class[c]:
            for t in machine.input_alphabet:
                mtr = (machine.transition[(v, t)]).pop()
                machine.transition[(v, t)].add(mtr)
                res.transition[(str(c), t)] = str(class_by_vertex[mtr])
    for s in  machine.finite_states:
        res.finite_states.add(str(class_by_vertex[s]))
    res.initial_state= str(class_by_vertex[machine.initial_state])
    return res

def main():
    #fsm1 = copy.deepcopy(read_fsm("task2_example1.txt"))
    fsm1 = copy.deepcopy(read_fsm(sys.argv[1]))
    wfile = open(sys.argv[1] + ".out", 'w')
    #wfile = open("task2_example1.txt" + ".out", 'w')
    wfile.write(minimize(make_full(fsm1)).print())

if __name__ == "__main__":
    main()
