'''
circuit_parser.py

File contains a function to parse a circuit containing the following elements:
R: resistor, one parameter in parentheses specifying resistance in ohms
C: capacitor, one parameter in parentheses specifying capacitance in microfarads
CPE: constant phase element, two parameters in parentheses specifying Q and n
Zw: Warburg impedance, one parameter in parentheses specifying the Warburg coefficient
+: puts the circuit elements in series
para: elements in parentheses are in parallel
'''
from impedance_calculator import capacitor, warburg, cpe, resistor

def parse_input(input_str):
    '''
    Function parses input in the form detailed above. Recursion is used to deal with parallel circuits.
    '''
    parameters = [[], []]  # keep track of the impedance functions and parameters
    in_para = False        # for skipping over the stuff in a para()
    in_element = False     # for skipping over the stuff in an element
    for i, v in enumerate(input_str):
        if in_para and input_str[i:i+4] == ')) +' or input_str[i:i+3] == ')),':
            in_para = False
        elif in_element and v == ')':  # close parantheses indicates end of an element
            in_element = False
        elif not in_para and not in_element and v not in ['+', ' ', ')']:
            if v == 'p': # start of a para, obtain each path and parse recursively
                path1_end = input_str.find('),', i)+1
                path2_end = input_str.find(')) +', i)
                
                if path2_end <= 0:
                    path2_end = len(input_str) - 1

                path1_params = parse_input(input_str[i+5:path1_end])
                path2_params = parse_input(input_str[path1_end+2:path2_end+1])
                parameters[0].append((path1_params[0], path2_params[0]))
                parameters[1].append((path1_params[1], path2_params[1]))
                in_para = True
            elif v == 'R': # resistor, grab the resistance from within the parentheses
                parameters[0].append(resistor)
                parameters[1].append(float(input_str[i+2:input_str.find(')', i)]))
                in_element = True
            elif v == 'C' and input_str[i+1] != 'P': # capacitor, grab capacitance and multiply by 1e-6
                parameters[0].append(capacitor)
                parameters[1].append(1e-6 * float(input_str[i+2:input_str.find(')', i)]))
                in_element = True
            elif v == 'Z': # warburg impedance, grab warburg coefficient
                parameters[0].append(warburg)
                parameters[1].append(float(input_str[i+3:input_str.find(')', i)]))
                in_element = True
            elif input_str[i:i+2] == 'CP': # constant phase element, need to get Q and n, separated by a comma
                comma = input_str.find(',', i)
                
                parameters[0].append(cpe)
                parameters[1].append((float(input_str[i+4:comma]), float(input_str[comma+2:input_str.find(')', comma)])))
                in_element = True
            else: # reach here - element is invalid, determine element name and print
                end = input_str.find('(', i)
                in_element = True
                print(f'{input_str[i:end]}: Invalid element encountered. Check the input circuit!')

    return parameters