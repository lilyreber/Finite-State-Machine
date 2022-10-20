import copy
import sys
import ply.yacc as yacc

from parser_fsm import *
global dka1
global dka2
global wfile
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

def printer(states, input_alphabet, initial_state, finite_state, transition):

    out = "STATES ="+str(states)+"\n"
    out+="ALPHABET ="+str(input_alphabet)+"\n"
    out+="INITIAL = {"+str(initial_state)+"}"+"\n"
    if len(finite_state)==0:
        out+="FINITE = {}"+"\n"
    else:
        out+="FINITE = "+str(finite_state)+"\n"
    for s in states:
        for symb in input_alphabet:
            out+="("+str(s)+")"+" ++ "+"\""+symb+"\""+" -> "+"("+str(transition[(s, symb)])+")"+"\n"
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
                        transit[((s1, s2), symb)] = (temp1, temp2)
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
    wfile.write(printer(states, input_alphabet, initial_state, finite_states, transition_new))


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
    wfile.write(printer(states, input_alphabet, initial_state, finite_states, transition_new))


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
    wfile.write(printer(states, input_alphabet, initial_state, finite_states, transition_new))


def addition():
    global dka1
    global dka2
    global wfile
    finite_states = set()
    for s in dka1.states:
        if s not in dka1.finite_states:
            finite_states.add(s)
    wfile.write(printer(dka1.states, dka1.input_alphabet, dka1.input_alphabet, finite_states, dka1.transition))



def main():
    global dka1
    global dka2
    global wfile
    dka1=FSM()
    dka2=FSM()
    sys.argv += ["intersection", "ex2.txt", "ex2_2.txt"]
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
