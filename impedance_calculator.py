import numpy as np

def resistor(w, R):
    '''
    Calculate the impedance of a resistor. Provided to make tracking elements easier by using function pointers. 
    '''
    return R + 0j

def capacitor(w, C):
    '''
    Calculate capacitor impedance given capacitance and frequency. 
    '''
    return -1j/(C*w)

def cpe(w, Q, n):
    '''
    Calculate constant phase element impedance given frequency, Q, and n. Euler's relation is used to compute e raise to a complex power. 
    '''
    return 1/(Q*w**n) * np.cos(-np.pi / 2 * n) + 1j/(Q*w**n) * np.sin(-np.pi / 2 * n)

def warburg(w, A):
    '''
    Calculate Warburg impedance given a Warburg coefficient and frequency
    '''
    return (A/w**(1/2)) * (1-1j)

def calculate_circuit_impedance(parameters, w):
    '''
    Function combines various circuit elements (in series or in parallel) and calculates the net impedance of the circuit. Recursion is used to calculate the impedances of each parallel path, which are then combined as reciprocals to give the impedance of the parallel section. 
    '''
    net_impedance = 0
    for element in zip(parameters[0], parameters[1]):
        if 'tuple' not in str(type(element[0])):
            if 'tuple' not in str(type(element[1])):
                net_impedance += element[0](w, element[1])
            else:
                net_impedance += element[0](w, *element[1])
        else:
            path1_parameters = [element[0][0], element[1][0]]
            path2_parameters = [element[0][1], element[1][1]]

            path1_impedance = calculate_circuit_impedance(path1_parameters, w)
            path2_impedance = calculate_circuit_impedance(path2_parameters, w)

            net_impedance += 1/(1/path1_impedance + 1/path2_impedance)

    return net_impedance

