import ply.yacc as yacc
import sys
import re
import copy

from lexer import tokens


class FSM:
    states = set()
    input_alphabet = set()
    initial_state = None
    finite_states = set()
    transition = dict()

    def print(self):
        out = "Finite state machine consist:\n"
        out += "States: " + '; '.join(self.states) + "\n"
        out += "Start: " + self.initial_state + "\n"
        out += "Finite states: " + '; '.join(self.finite_states) + "\n"
        out += "Alphabet: " + '; '.join(self.input_alphabet) + "\n"
        out += "Rules: \n"
        for x in self.transition:
            for y in self.transition[x]:
                out += f"{x[0]}------\"{x[1]}\"------>{y}\n"
        return out

    def clear(self):
        self.states.clear()
        self.input_alphabet.clear()
        self.initial_state = None
        self.finite_states.clear()
        self.transition.clear()


fsm_global = FSM()

def p_error(p):
    if p == None:
        print("end of file")
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
    print(f"Syntax error: Unexpected {token}")


def p_states(p):
    'start : STATES ASSIGNMENT SET'
    fsm_global.states = set([state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3])])


def p_alphabet(p):
    'start : ALPHABET ASSIGNMENT SET'
    fsm_global.input_alphabet = set([state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3])])


def p_start(p):
    'start : INITIAL ASSIGNMENT SET'
    s = [state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3]) ]
    if len(s) != 1:
        print ("invalid initial state: " + p[3])
        fsm_global.initial_state = s[0]
    else:
        fsm_global.initial_state = p[3]


def p_finite(p):
    'start : FINITE ASSIGNMENT SET'
    for state in re.split(r'(?<!\\),', p[3]):
        state = state.replace('\,', ',')
        if state in fsm_global.states:
            fsm_global.finite_states.add(state)
        else:
            print("invalid finite state: " + state)


def p_transition(p):
    'start : STATE BINDING SYMBOL TRANSITION STATE'
    if p[1] not in fsm_global.states:
        return print(p[1] + " is not state")
    if p[3] not in fsm_global.input_alphabet and p[3] != "":
        return print(p[3] + " is not in alphabet")
    if p[5] not in fsm_global.states:
        return print(p[5] + " is not state")
    if (p[1], p[3]) not in fsm_global.transition:
        fsm_global.transition[(p[1], p[3])] = set()
    fsm_global.transition[(p[1], p[3])].add(p[5])



def read_fsm(file):
    fsm_global.clear()
    parser = yacc.yacc()
    rfile = open(file)
    wfile = open(file + ".out", 'w')
    for line in rfile.readlines():
        parser.parse(line)
    wfile.write(fsm_global.print())
    return fsm_global

def main():
    read_fsm(sys.argv[1])


if __name__ == "__main__":
    main()
