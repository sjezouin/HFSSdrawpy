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
from scripts.designer import Circuit, KeyElt, ConnectElt

project = get_active_project()
design = project.get_active_design()
modeler = design.modeler

modeler.set_units('mm')

c = Circuit(design, modeler)

###########################################################
################# DRAWING STARTS HERE #####################
###########################################################

#KeyElt.is_overdev =True
#KeyElt.overdev = parse_entry('0.5um')

########## PCB, Chip and Ground Plane ###########
c.set_variable("chip_width", "8.67mm")
c.set_variable("chip_length", "8.12mm")
c.set_variable("chip_thickness", "280um")
c.set_variable("pcb_thickness", "320um")
c.set_variable('vaccuum_thickness', 6*c.chip_thickness)

c.draw_box('pcb', [0, 0, -c.chip_thickness], [c.chip_width, c.chip_length, -c.pcb_thickness], "Rogers TMM 10i (tm) no loss")
c.draw_box('chip', [0, 0, 0], [c.chip_width, c.chip_length, -c.chip_thickness], 'silicon')
c.draw_box('box', [0, 0, 0], [c.chip_width, c.chip_length, c.vaccuum_thickness], 'vacuum')

c.draw_rect('ground_plane', [0, 0], [c.chip_width, c.chip_length])
c.assign_perfE(c.ground_plane)


######### Connectors #######

con1, con2, con3, con4, con5 = '4.06mm', '3.01mm', '7.54mm', '3.01mm', '6.36mm'
KeyElt.pcb_track, KeyElt.pcb_gap = parse_entry('300um'), parse_entry('200um')
bond_length, bond_slope = '200um', '0.5'
c.set_variable('track', '84um')
c.set_variable('gap', '50um')


#
c.key_elt('in_right', [con3, c.chip_length], [0, -1])
c.key_elt('flux_right', [con2, c.chip_length], [0, -1])

c.key_elt('in_left', [con5, 0], [0, 1])
c.key_elt('flux_left', [con4, 0], [0, 1])

c.in_right.draw_connector(c.track, c.gap, bond_length, bond_slope)
c.flux_right.draw_connector(c.track, c.gap, bond_length, bond_slope)
c.in_left.draw_connector(c.track, c.gap, bond_length, bond_slope)
c.flux_left.draw_connector(c.track, c.gap, bond_length, bond_slope)

c.set_variable('Lj_down', '0.16nH')
c.set_variable('Lj_up', '0.138nH')
c.set_variable('squid_track', '5um')

snail_dict={'loop_width':20e-6, 'loop_length':20e-6, 'length_big_junction':10e-6, 'length_small_junction':2e-6, 'bridge':1e-6, 'bridge_spacing':1e-6}

c.set_variable('offsetX_squid_right', '5mm')
c.set_variable('offsetY_squid_right', '3mm')
c.key_elt('squid_right', [c.chip_width-c.offsetX_squid_right, c.chip_length-c.offsetY_squid_right], [1,0])
c.squid_right.draw_snails(c.track, c.gap, '450um', '70um', c.track, c.gap,
                          iTrackSnail=c.squid_track, N_snails=1,
                          snail_dict=snail_dict, fillet=True, L_eq='1.6nH')

c.set_variable('offsetX_squid_left', '4.5mm')
c.set_variable('offsetY_squid_left', '3mm')
c.key_elt('squid_left', [c.chip_width-c.offsetX_squid_left, c.offsetY_squid_left], [-1,0])
c.squid_left.draw_snails(c.track, c.gap, '450um','70um', c.track, c.gap,
                         iTrackSnail=c.squid_track, N_snails=1,
                         snail_dict=snail_dict, fillet=True, L_eq='1.4nH')


c.set_variable('length_right', '2.25mm')
c.set_variable('length_left', '2.86mm')

c.set_variable("capa_right_spacing", '0.01mm')
c.set_variable("capa_right_width", c.track/2)
c.set_variable("capa_right_length", '0.4mm')
c.key_elt('capa_right', c.squid_right.pos+[c.length_right/2, 0], [-1,0])
c.capa_right.draw_capa_inline(c.track, c.gap, c.capa_right_length, c.capa_right_spacing, n_pad=5)

c.set_variable("capa_left_spacing", c.capa_right_spacing)
c.set_variable("capa_left_width", c.track/2)
c.set_variable("capa_left_length", '0.4mm')
c.key_elt('capa_left', c.squid_left.pos+[c.length_left/2, 0], [-1,0])
c.capa_left.draw_capa_inline(c.track, c.gap, c.capa_left_length, c.capa_left_spacing, n_pad=5)


c.key_elt('end_right', c.squid_right.pos-[c.length_right/2, 0], [1,0])
c.end_right.draw_end_cable(c.track, c.gap, typeEnd = 'open')

c.key_elt('end_left', c.squid_left.pos-[c.length_left/2, 0], [1,0])
c.end_left.draw_end_cable(c.track, c.gap, typeEnd = 'open')

c.set_variable('fillet', '0.2mm')

c.connect_elt('in_cable_right', 'capa_right_2', 'in_right')
c.in_cable_right.draw_cable(fillet=c.fillet)
c.connect_elt('in_cable_left', 'capa_left_2', 'in_left')
c.in_cable_left.draw_cable(fillet=c.fillet)


c.connect_elt('flux_cable_right', 'flux_right', 'squid_right_pump')
c.flux_cable_right.draw_cable(fillet=c.fillet)
c.connect_elt('flux_cable_left', 'flux_left', 'squid_left_pump')
c.flux_cable_left.draw_cable(fillet=c.fillet)

c.set_variable('meander_length_right', '0.56mm')
c.connect_elt('res1_right', 'capa_right_1', 'squid_right_1')
c.res1_right.draw_cable(fillet=c.fillet, is_meander=False, to_meander=[1, 1], meander_length=c.meander_length_right)
c.connect_elt('res2_right', 'end_right', 'squid_right_2')
c.res2_right.draw_cable(fillet=c.fillet, is_meander=False, to_meander=[1, 1], meander_length=c.meander_length_right)

c.set_variable('meander_length_left', '0.653mm')
c.connect_elt('res1_left', 'squid_left_2', 'capa_left_1')
c.res1_left.draw_cable(fillet=c.fillet, is_meander=False, to_meander=[1, 1], meander_length=c.meander_length_left)
c.connect_elt('res2_left', 'end_left', 'squid_left_1')
c.res2_left.draw_cable(fillet=c.fillet, is_meander=False, to_meander=[1, 1], meander_length=c.meander_length_left)


######## UNITE - SUBSTRACT - PerfE #####
#Finalisation globale du dessin

for obj in c.trackObjects:
    c.assign_perfE(obj)
gapObject = c.unite(c.gapObjects)
c.subtract(c.ground_plane, [gapObject])

release()