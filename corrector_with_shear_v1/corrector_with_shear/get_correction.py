import networkx as nx

def get_correction(matches, template, d, shear):
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
        rows_eq = pair[0][0] == pair[1][0] # This makes rows_eq = True for each pair that it's true for
        cols_eq = pair[0][1] == pair[1][1] # This makes cols_eq = True for each pair that it's true for
        # Then we can perform processes on each pair depending on whether rows_eq or cols_eq is true.
        if shear == 0:
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
        elif shear !=0:
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
            elif cols_eq:
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
            elif (abs(pair[0][1]-pair[1][1]) == d-1 and abs(pair[0][0]-pair[1][0])) == shear:
                # this denotes a horizontal crossing on a sheared graph, we'll want 'h' of the greatest row value
                if pair[0][1] > pair[1][1]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'h'))
                elif pair[0][1] < pair[1][1]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'h'))
            elif (abs(pair[0][1]-pair[1][1]) == shear and abs(pair[0][0]-pair[1][0])) == d-1:
                # this denotes a vertical crossing on a sheared graph, we want 'v' of the greatest row value
                if pair[0][0] > pair[1][0]:
                    qubit_addresses.append((pair[0][0], pair[0][1], 'v'))
                elif pair[0][0] < pair[1][0]:
                    qubit_addresses.append((pair[1][0], pair[1][1], 'v'))
            # now corner cases: 
            elif ((abs(pair[0][0]-pair[1][0])) == d-1 and abs(pair[0][1]-pair[1][1]) == d-1):
                # this is the very 4 corners
                mod = shear%d
                if mod < d/2:
                    if pair[0][0]==pair[0][1]:
                        qubit_addresses.append((d-1, d-1, 'v'))
                    elif pair[0][0]!=pair[0][1]:
                        qubit_addresses.append((0, d-1, 'h'))
                elif mod > d/2:
                    if pair[0][0]==pair[0][1]:
                        qubit_addresses.append((d-1, d-1, 'h'))
                    elif pair[0][0]!=pair[0][1]:
                        qubit_addresses.append((d-1, 0, 'v'))
                elif mod == d/2:
                    assert 0
            # next these aren't the very corners but next to them    
            elif (abs(pair[0][0]-pair[1][0])) == d-1:
                    if pair[0][0] > pair[1][0]:
                        qubit_addresses.append((pair[0][0], pair[0][1], 'v'))
                    elif pair[1][0] > pair[0][0]:
                        qubit_addresses.append((pair[1][0], pair[1][1], 'v'))
            elif (abs(pair[0][1]-pair[1][1])) == d-1:
                    if pair[0][1] > pair[1][1]:
                        qubit_addresses.append((pair[0][0], pair[0][1], 'h'))
                    elif pair[0][1] < pair[1][1]:
                        qubit_addresses.append((pair[1][0], pair[1][1], 'h'))
    return set(qubit_addresses), paths