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
c.key_elt('pads', [0, 0], [1,0])
pos_b = [(0,0),(2500,0),(0,2500),(2500,2500)]
#
#bridge_spacing = '5um'
#c.pads.draw_dose_test(['100um', '100um'], '50um', '3um', '1.5um', 1, bridge_spacing, '10um', '2um')

if 1==1:
    for ib, valb in enumerate(np.array([1, 5, 10, 15])): # number of snails
        for isp, valsp in enumerate(np.array([3.5, 4, 4.5, 5, 5.5])): # bridge spacing
            pos_y = str(isp*400)+'um'
            pos_x = str(ib*1500)+'um'
            c.key_elt('pads', [pos_x,pos_y], [1,0])
            bridge_spacing = str(valsp)+'um'
            c.pads.draw_dose_test(['100um', '100um'], '1000um', '5um', '1.5um', valb, bridge_spacing, '10um', '2um')
    
    for isp2, valsp2 in enumerate(np.linspace(0,1,10)): # bridge spacing
        for il2, vall2 in enumerate([2, 10]): # length bridge
            x0, y0 = [0, 2000]
            pos_x = str(x0+isp2*400)+'um'
            pos_y = str(y0+il2*200)+'um'
            c.key_elt('pads', [pos_x,pos_y], [1,0])
            width = str(vall2)+'um' # length bridge
            c.pads.draw_dose_test_junction(['100um', '100um'], '50um', width,
                                           '1500nm', n_bridge=1,
                                           spacing_bridge='3um')
            
    for isp3, valsp3 in enumerate(np.array([3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7])): # bridge spacing
        for il3, vall3 in enumerate([10]): # length bridge
            x0, y0 = [0, 2500]
            pos_x = str(x0+isp3*400)+'um'
            pos_y = str(y0+il3*200)+'um'
            c.key_elt('pads', [pos_x,pos_y], [1,0])
            width = str(vall3)+'um' # length bridge
            c.pads.draw_dose_test_junction(['100um', '100um'], '50um', width,
                                           '1500nm', n_bridge=2,
                                           spacing_bridge=str(valsp3)+'um')
            
    for i3, val3 in enumerate([1,2,3,4,5,6,7,8,9,10]): # length bridge
        for il3, vall3 in enumerate([2, 10]): # length bridge
            x0, y0 = [0, 3000]
            pos_x = str(x0+i3*400)+'um'
            pos_y = str(y0+il3*200)+'um'
            c.key_elt('pads', [pos_x,pos_y], [1,0])
            width = str(vall3)+'um' # length bridge
            c.pads.draw_dose_test_junction(['100um', '100um'], '50um', width,
                                           '0nm', n_bridge=1,
                                           spacing_bridge='1um')