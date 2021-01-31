### Lattice class for a lattice object with qubits and checks (in dictionary formats) ###
### Initiate Lattice, apply error or specific operator, and correct ###
### At any point, display with dump() method which prints out the lattice as an array ###

import networkx as nx
import numpy as np
import collections
import itertools
from random import random
from corrector.Pauli import Pauli
from corrector.get_correction import get_correction

def nx_template(d, shear):
    # This just makes an nx graph with the right boundary conditions and weighted edges, for use in MWPM
    # Is prepped for changing shear
    G = nx.Graph()
    for row in range(d-1):
        for col in range(d):
            G.add_edge((row, col), (row, (col+1)%d), weight=1)
            G.add_edge((row, col), ((row+1)%d, col), weight=1)
    row = d-1
    for col in range(d):
        G.add_edge((row, col), (row, (col+1)%d), weight=1)
        G.add_edge((row, col), ((row+1)%d, (col+shear)%d), weight=1)
    assert len(G.edges) == 2*(d**2)
    return G

def win_or_lose(BA, H, V, verbose=False):
    cond1 = BA.commutes(H)
    cond2 = BA.commutes(V)
    if cond1 and cond2:
        if not verbose:
            return True
        else:
            print("win!")
            print("BA commutes with horizontal operator:", cond1)
            print("BA commutes with vertical operator:", cond2)
    else:
        if not verbose:
            return False
        else:
            print("lose")
            print("BA commutes with horizontal operator:", cond1)
            print("BA commutes with vertical operator:", cond2)

class Lattice:
    def __init__(self, d, shear):
        self.d = d
        self.shear = shear
        self.n = 2*(d**2)
        Qubits = collections.OrderedDict() #N.B. qubits are ordered h, v for each check (not line by line)
        for row in range(d):
            for col in range(d):
                address = (row, col, 'h')
                Qubits[address] = 0
                address = (row, col, 'v')
                Qubits[address] = 0
        self.q = Qubits
        Checks = collections.OrderedDict()
        for row in range(self.d):
            for col in range(self.d):
                Checks[row, col] = 0
        self.c = Checks
    def __str__(self):
        return str(("Qubit lattice", self.d, self.n))
    __repr__ = __str__
    def light_checks(self):
        # NB need to change this function when changing shear!
        if self.shear == 0:
            for row in range(self.d):
                for col in range(self.d):
                    val = (self.q[(row, col, 'h')] + self.q[(row, col, 'v')] +  self.q[(row, (col-1)%self.d, 'h')] + self.q[((row-1)%self.d, col, 'v')] ) %2
                    if val:
                        self.c[row, col] = 1
                    else:
                        self.c[row, col] = 0
        else:
            assert 0
    def apply_error(self, threshold):
        errop = ''
        for qubit in list(self.q.keys()):
            if random() < threshold:
                self.q[qubit] = (self.q[qubit]+1)%2
                errop += 'X'
            else:
                errop += 'I'
        assert len(self.q) == len(errop)
        self.error = Pauli(1, errop)
        self.light_checks()
    def apply_op(self, Pauli):
        assert len(self.q) == len(Pauli.op)
        for i, qubit in enumerate(list(self.q.keys())):
            if Pauli.op[i] == 'X':
                self.q[qubit] = (self.q[qubit]+1)%2
        self.light_checks()
    def apply_op_z(self, Pauli):
        assert len(self.q) == len(Pauli.op)
        for i, qubit in enumerate(list(self.q.keys())):
            if Pauli.op[i] == 'Z':
                self.q[qubit] = 'Z'
    def dump(self):
        d = self.d*2
        A = np.empty((d, d), dtype=object)
        index = 0
        for i in range(0, d, 2):
            for j in range(0, d, 2):
                ### checks ###
                index += 1
                if list(self.c.values())[index-1] == 1:
                    A[i,j]='*'
                elif list(self.c.values())[index-1] == 0:
                    A[i,j]='+'
                else:
                    assert 0
        horiz = []
        verts = []
        for n, qubit in enumerate(list(self.q.values())):
            if n%2 == 0:
                horiz.append(qubit)
            elif n%2 == 1:
                verts.append(qubit)
            else:
                assert 0
        index = 0
        for i in range(0, d, 2):
            for j in range(1, d, 2):
                ### horiz qubits ###
                index += 1
                if horiz[index-1] == 1:
                    A[i,j]='X'
                elif horiz[index-1] == 0:
                    A[i,j]="-"
                elif horiz[index-1] == 'Z':
                    A[i,j]="Z"
                else:
                    assert 0
        index = 0
        for i in range(1, d, 2):
            for j in range(0, d, 2):
                ### vert qubits ###
                index += 1
                if verts[index-1] == 1:
                    A[i,j]='X'
                elif verts[index-1] == 0:
                    A[i,j]="|"
                elif verts[index-1] == 'Z':
                    A[i, j]="Z"
                else:
                    assert 0
        for i in range(1, d, 2):
            for j in range(1, d, 2):
                A[i,j]=' '
        A = str(A)
        A = A.replace("'", " ")
        print(A)
    def show_op(self, Pauli):
        # shows what the operator would look like if enacted on a fresh lattice (all qubits = 0)
        A = Lattice(self.d, self.shear)
        assert len(self.q) == len(Pauli.op)
        if 'Z' in Pauli.op:
            A.apply_op_z(Pauli)
        else:
            A.apply_op(Pauli)
        return A.dump()
    def correct(self, nx_template):
        lit_checks = []
        for key, value in self.c.items():
            if value == 1:
                lit_checks.append(key)
        self.lit_checks = lit_checks
        different_pairs = list(itertools.combinations(lit_checks, 2))
        self.T = nx_template
        M = nx.Graph()
        self.M = M
        for pair in different_pairs:
            path = nx.shortest_path(self.T, pair[0], pair[1], weight='weight')
            distance = -(len(path)-1)
            M.add_edge(pair[0], pair[1], weight=distance)
        matches = nx.max_weight_matching(self.M, True)
        self.matches = matches
        qubit_addresses, paths = get_correction(self.matches, self.T, self.d)
        self.q_a = qubit_addresses
        self.paths = paths
        for address in qubit_addresses:
            self.q[address] = (self.q[address]+1)%2
        self.light_checks()
        corrop = ''
        for i, qubit in enumerate(list(self.q.keys())):
            if qubit in qubit_addresses:
                corrop += 'X'
            else:
                corrop += 'I'
        self.correction = Pauli(1, corrop)
        self.BA = self.correction*self.error
        return self.BA
    def logical_operators(self):
        hop = ''
        vop = ''
        horiz=[(2*n)+1 for n in range(self.d)]
        self.horiz = horiz
        vert=[(self.d*2*n) for n in range(self.d)]
        self.vert = vert
        for i in range(self.n):
            if i in horiz:
                hop += 'Z'
            else:
                hop += 'I'
            if i in vert:
                vop += 'Z'
            else:
                vop += 'I'
        self.H = Pauli(1, hop)
        self.V = Pauli(1, vop)
        return self.H, self.V