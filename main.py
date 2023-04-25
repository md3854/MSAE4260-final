from circuit_parser import parse_input
from impedance_calculator import calculate_circuit_impedance
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backend_bases import MouseButton

instructions = '''
EIS Simulator
Max Dickman, Khushi Kabra, Maya Schuchert

Type in your circuit and a frequency range to generate a Nyquist plot. The following elements can be used in a circuit:
- Resistor (R)
- Capacitor (C)
- Constant phase element (CPE)
- Warburg impedance (Zw)

To specify the parameters for an element (e.g. resistance of a resistor), type the number in parentheses following the element symbol (e.g. R(10) for a 10 Ω resistor). Note that capacitance is entered in microfarads. Combine elements in series with a '+' sign between them. Combine elements in parallel using para() and comma-separating the two parallel paths. 

You can view Z', Z", and ω by left clicking on the plot. Right click to remove the tooltip. 

Example: R(10) + para(R(100) + Zw(50), C(1)) represents a circuit with an electrolyte resistance of 10 Ω, a diffusion resistance of 100 Ω, a Warburg impedance with a Warburg coefficient of 50 Ω s^(-1/2), and a double layer capacitance of 1 μF in parallel with Rd and Zw. 
'''

def main():
    '''
    Function runs the overall EIS simulator by gathering input and calling functions in the correct order. Also writes data to a text file
    '''
    print(instructions)
    circuit = input('Enter the circuit: ')
    w_start = float(input('Enter the starting frequency: '))
    w_end = float(input('Enter the ending frequency: '))
    filename = input('Enter the filepath to store the data: ')
    parameters = parse_input(circuit)
    impedances, freq_list = plot_values(np.log10(w_start), np.log10(w_end),
                                        parameters)
    
    # write data to a text file
    with open(filename, 'w') as f:
        for i in impedances:
            f.write(str(i) + '\n')
        f.write('\n')
        for i in freq_list:
            f.write(str(i) + '\n')

def plot_values(w_start, w_end, parameters):
    '''
    Function calculates the impedance at frequencies within the range specified and plots them using maptlotlib. 
    '''
    # define frequency range and empty array for impedances
    freq_list = np.logspace(w_start, w_end, num=100) * 2 * np.pi
    impedances = np.zeros(len(freq_list), dtype=complex)

    # calculate impedances
    for i, w in enumerate(freq_list):
        impedances[i] = calculate_circuit_impedance(parameters, w)

    # separate Z' and Z"
    real_list = impedances.real
    imag_list = impedances.imag

    # plot the data, flip the y-axis
    fig, ax = plt.subplots()
    ax.plot(real_list, imag_list, marker='.', picker=True, pickradius=5)
    ax.set_xlim([-10, max(real_list) + 50])
    ax.set_ylim(tuple([-1 * i for i in plt.xlim()]))

    # annotation used to show data on click
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"))
    annot.set_visible(False)

    def on_pick(event):
        '''
        Event handler that displays Z', Z", and ω when a point on (or near) the plot is clicked. 
        '''
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind[0]
            real = round(xdata[ind], 2)
            imag = round(ydata[ind], 2)
            freq = round(freq_list[ind]*2*np.pi, 2)

            annot.xy = [xdata[ind], ydata[ind]]
            text = f'Z\' = {real:<5} Ω\nZ" = {imag:<6} Ω\nω = {freq:<9} Hz'
            annot.set_text(text)
            annot.set_visible(True)
            fig.canvas.draw_idle()

    def on_click(event):
        '''
        Event handler that removes the annotation on right click
        '''
        if event.inaxes and event.button is MouseButton.RIGHT:
            annot.set_visible(False)
            fig.canvas.draw_idle()

    # connect the event handlers to their actions
    plt.connect('pick_event', on_pick)
    plt.connect('button_press_event', on_click)

    plt.show()

    return impedances, freq_list

if __name__ == '__main__':
    main()