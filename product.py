import copy
import sys
import ply.yacc as yacc

from parser_fsm import *
from minimization import *
global dka1
global dka2
global wfile
def add_slash(t):
    return t.replace("\\", "\\\\").replace("(", "\(").replace(")", "\)").replace("{", "\{").replace("}", "\}").replace('"', '\"').replace('"', '\"')
def alphabet_association():
    lang=set()
    for s1 in dka1.input_alphabet:
        lang.add(s1)
    for s2 in dka2.input_alphabet:
        lang.add(s2)
    return lang
def reading_dka1():
    temp = read_fsm(sys.argv[2])
    dka1.states = copy.deepcopy(temp.states)
    dka1.input_alphabet = copy.deepcopy(temp.input_alphabet)
    dka1.initial_state = copy.deepcopy(temp.initial_state)
    dka1.transition = copy.deepcopy(temp.transition)
    dka1.finite_states = copy.deepcopy(temp.finite_states)

def reading_dka2():
    temp = read_fsm(sys.argv[3])
    dka2.states = copy.deepcopy(temp.states)
    dka2.input_alphabet = copy.deepcopy(temp.input_alphabet)
    dka2.initial_state = copy.deepcopy(temp.initial_state)
    dka2.transition = copy.deepcopy(temp.transition)
    dka2.finite_states = copy.deepcopy(temp.finite_states)

def printer(res):

    out = res.print_as_fsm()

    return out

def product_of_states():
    states = set()
    global dka1
    global dka2
    for s1 in dka1.states:
        for s2 in dka2.states:
            states.add((s1, s2))
    return states


def transition():
    transit = dict()
    global dka1
    global dka2
    for s1 in dka1.states:
        for s2 in dka2.states:
            for symb in dka1.input_alphabet:
                for temp1 in dka1.transition[(s1, symb)]:
                    for temp2 in dka2.transition[(s2, symb)]:
                        temp_v=set()
                        temp_v.add((temp1, temp2))
                        transit[((s1, s2), symb)] = temp_v
    return transit


def intersection():
    global dka1
    global dka2
    global wfile
    states = product_of_states()
    initial_state = (dka1.initial_state, dka2.initial_state)

    finite_states = set()
    for (s1, s2) in states:
        finite_states1 = s1 in dka1.finite_states
        finite_states2 = s2 in dka2.finite_states
        if finite_states1 and finite_states2:
            finite_states.add((s1, s2))
    input_alphabet = alphabet_association()
    transition_new = transition()
    res= FSM()

    res.transition=transition_new
    res.states=states
    res.initial_state=initial_state
    res.finite_states=finite_states
    res.input_alphabet=input_alphabet
    res = minimize(res)
    wfile.write(printer(res))


def association():
    global dka1
    global dka2
    global wfile
    states = product_of_states()

    initial_state = (dka1.initial_state, dka2.initial_state)

    finite_states = set()

    for (s1, s2) in states:
        finite_states1 = s1 in dka1.finite_states
        finite_states2 = s2 in dka2.finite_states
        if finite_states1 or finite_states2:
            finite_states.add((s1, s2))
    input_alphabet = alphabet_association()
    transition_new = transition()
    res = FSM()

    res.transition = transition_new
    res.states = states
    res.initial_state = initial_state
    res.finite_states = finite_states
    res.input_alphabet = input_alphabet
    res = minimize(res)
    wfile.write(printer(res))


def difference():
    global dka1
    global dka2
    global wfile
    states = product_of_states()

    initial_state = (dka1.initial_state, dka2.initial_state)

    finite_states = set()

    for (s1, s2) in states:
        finite_state1 = s1 in dka1.finite_states
        finite_state2 = s2 in dka2.finite_states
        if finite_state1 ^ finite_state2:
            finite_states.add((s1, s2))

    input_alphabet = alphabet_association()
    transition_new = transition()
    res = FSM()

    res.transition = transition_new
    res.states = states
    res.initial_state = initial_state
    res.finite_states = finite_states
    res.input_alphabet = input_alphabet
    res = minimize(res)
    wfile.write(printer(res))


def addition():
    global dka1
    global dka2
    global wfile
    finite_states = set()
    for s in dka1.states:
        if s not in dka1.finite_states:
            finite_states.add(s)
    res = FSM()

    res.transition = dka1.transition
    res.states = dka1.states
    res.initial_state = dka1.initial_state
    res.finite_states = finite_states
    res.input_alphabet = dka1.input_alphabet
    res = minimize(res)
    wfile.write(printer(res))



def main():
    global dka1
    global dka2
    global wfile
    dka1=FSM()
    dka2=FSM()

    operation = sys.argv[1]
    wfile = open(sys.argv[2] +"_"+sys.argv[1] + ".out", 'w')
    if operation == "intersection":
        reading_dka1()
        reading_dka2()
        intersection()
    elif operation == "association":
        reading_dka1()
        reading_dka2()
        association()
    elif operation == "difference":
        reading_dka1()
        reading_dka2()
        difference()
    elif operation == "addition":
        reading_dka1()
        addition()
    else:
        print("Execution error: no such operation")


if __name__ == "__main__":
    main()
