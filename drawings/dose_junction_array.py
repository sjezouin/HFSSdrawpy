'''
TODO

- debug comments
- automate Bonds
- delete "mm", instead, select the units in HFSS
- define in classes
class CircuitElement(object):
    def __init__(self, gates, params):

    def get_gates(self):
        returns list of gates (inputs and outpts)

class Capacitor(CircuitElement):
    def draw(self):
        draws the element

- LitExp: check if variable exists, updates value if exists, create a new one if not.
- Create drawing script which can start from blank file
- Premesh

'''

'''
Assumption

- only assign lumpRLC to rectangles
- assume to have list and not tuples for polylines
- TODO, do not do Lj+'1nH' for now, but can do bx+'1mm'
'''



from scripts.hfss import get_active_project, release, parse_entry
from scripts.designer import Circuit, KeyElt, ConnectElt, Vector
import numpy as np

project = get_active_project()
design = project.get_active_design()
modeler = design.modeler

modeler.set_units('mm')

c = Circuit(design, modeler)

KeyElt.is_mask = False
KeyElt.gap_mask = parse_entry('20um')
KeyElt.overdev = parse_entry('0.9um')

#######################
### DRAWING STARTS HERE 
#######################

pos_b = [(0,0),(2500,0),(0,2500),(2500,2500)]

for ib, valb in enumerate(np.array([1, 2, 3, 4])): # number of bridges
    for isp, valsp in enumerate(np.array([3.5, 4, 4.5, 5, 5.5])): # bridge spacing
        for il, vall in enumerate(np.arange(1, 10.1, 1)): # length bridge
            x0, y0 = pos_b[ib]
            pos_x = str(x0+isp*400)+'um'
            pos_y = str(y0+il*200)+'um'
            c.key_elt('pads', [pos_x,pos_y], [1,0])
            width = str(vall)+'um' # length bridge
            c.pads.draw_dose_test_junction(['100um', '100um'], '50um', width,
                                           '1500nm', n_bridge=valb,
                                           spacing_bridge=str(valsp)+'um')
