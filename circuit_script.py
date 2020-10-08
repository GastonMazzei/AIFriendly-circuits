import matplotlib.pyplot as plt

# http://www.ecircuitcenter.com/Circuits.htm
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from pathlib import Path
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import SubCircuitFactory
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *
from PIL import Image
from matplotlib.pyplot import imshow
%matplotlib inline
import numpy as np


libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

name = 'hw_rectifier_opamp'
parser = SpiceParser(f'/home/m4zz31/Documents/circuits/CASO1/{name}.cir')
circuit = parser.build_circuit(ground='0') 
circuit.include(spice_library['LM741']) #NOT
#print(circuit)
#image = Image.open(f'/home/m4zz31/Documents/circuits/{name}.png') 
#imshow(np.asarray(image))
figure, ax = plt.subplots(figsize=(20, 10))
ax.grid()
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')
plt.tight_layout()
circuit.include(spice_library['D1N4148']) #981

deter = True

if deter:
    A = '4' 
    B = '1'
    circuit.X('extradiode','D1N4148', A, B)
    circuit.D('tester_diode', A, B, model='D1N4148')
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=0.1@u_ms, end_time=0.0008@u_s)

if deter:
    try: 
        ax.plot(analysis[B]-analysis[A])
        pass
    except:
        try: ax.plot(analysis[B])
        except: ax.plot(abs(analysis[A]))
ax.plot(analysis['1'])
ax.plot(analysis['3'])
if deter:
    ax.legend(('diode','in', 'out'), loc=(.8,.8))
else: ax.legend(('in', 'out'), loc=(.8,.8))
plt.show()


# from # http://www.ecircuitcenter.com/Circuits.htm
import random
import pandas as pd
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from pathlib import Path
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import SubCircuitFactory
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *
from PIL import Image
from matplotlib.pyplot import imshow
%matplotlib inline
import numpy as np
import itertools

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

def simulate_me(name,A,B):
    libraries_path = find_libraries()
    spice_library = SpiceLibrary(libraries_path)
    parser = SpiceParser(f'/home/m4zz31/Documents/circuits/CASO1/{name}.cir')
    circuit = parser.build_circuit(ground='0') 
    circuit.include(spice_library['D1N4148'])
    circuit.X('tester_diode','D1N4148', A, B)
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=5@u_us, end_time=2@u_ms)
    try:
        C = max(abs(analysis[B]-analysis[A]))
    except: 
        try: C = max(abs(analysis[B]))
        except: C = max(abs(analysis[A]))
    del(circuit)
    return C

treshold = 4
name = 'hw_rectifier_opamp'
a = [str(x) for x in list(circuit.nodes)]
a = [x for x in a if x!='100' and x!='101']
tabla = pd.DataFrame()

uno = list(itertools.combinations(a, 2))
dos = [(x[1],x[0]) for x in uno]
tres = uno+dos
for x in tres:
#for x in range(int(3*len(a))):
#for x in range(1):
    try: 
        #(A,B) = random.sample(a,2)
        (A,B) = x
        C = simulate_me(name,A,B)
        aux = [A,B,int(C)>treshold]    
        tabla = tabla.append(pd.DataFrame([aux]))
    except Exception as ins: 
        print('error at ',x)
        print(ins.args)
tabla.columns = ['Nodo 1', 'Nodo 2', 'Tension']
print(tabla)
