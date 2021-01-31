### This function works with the matches to return a list of qubit addresses to flip ###

import networkx as nx

def get_correction(matches, template, d):
    paths = []
    for pair in list(matches):
        paths.append(nx.shortest_path(template, pair[0], pair[1], weight='weight'))
    qubit_list = []
    for path in paths:
        z = len(path)
        for r in range(z-1):
            qubit_list.append([path[r], path[r+1]])
    qubit_addresses = []
    for pair in qubit_list:
        rows_eq = pair[0][0] == pair[1][0]
        cols_eq = pair[0][1] == pair[1][1]
        if rows_eq:
            assert not cols_eq
            if abs(pair[0][1]-pair[1][1]) == d-1:
                if pair[0][1] < pair[1][1]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'h'))
                elif pair[0][1] > pair[1][1]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'h'))
            else:
                if pair[0][1] < pair[1][1]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'h'))
                elif pair[0][1] > pair[1][1]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'h'))
        if cols_eq:
            assert not rows_eq
            if abs(pair[0][0]-pair[1][0]) == d-1:
                if pair[0][0] < pair[1][0]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'v'))
                elif pair[0][0] > pair[1][0]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'v'))
            else:
                if pair[0][0] < pair[1][0]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'v'))
                elif pair[0][0] > pair[1][0]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'v'))
    return qubit_addresses, paths