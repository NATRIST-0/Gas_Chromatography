"""
manim -pqm wheatstone_bridge.py WheatstoneBridge
"""

from manim import *
from manim_circuit import *

class WheatstoneBridge(Scene):
    def construct(self):
        circuit = Circuit()

        # Define components with explicit positioning
        r1 = Resistor("R1", direction=UP).shift(UP*2)
        r2 = Resistor("R2", direction=RIGHT).shift(RIGHT*2).rotate(-PI/2)
        r3 = Resistor("R3", direction=DOWN).shift(DOWN*2)
        r4 = Resistor("R4", direction=LEFT).shift(LEFT*2).rotate(-PI/2)

        # Add components to circuit
        circuit.add_components(r1, r2, r3, r4)

        # Add wires for the Wheatstone bridge
        circuit.add_wire(r1.get_terminals("right"), r2.get_terminals("left"), invert=True)
        circuit.add_wire(r2.get_terminals("right"), r3.get_terminals("right"))
        circuit.add_wire(r3.get_terminals("left"), r4.get_terminals("right"), invert=True)
        circuit.add_wire(r4.get_terminals("left"), r1.get_terminals("left"))

        # Rotate the bridge 45 degrees
        circuit.rotate(PI/4)

        # Add voltage source
        vin = VoltageSource(value="V_1", label=True, direction=UP, dependent=False).shift(LEFT*4)

        # Add voltage source to circuit
        circuit.add_components(vin)

        # Connect voltage source to the circuit with explicit coordinates
        # Custom define wires to have better control with how the junctions are generated
        circuit.add_wire(
            vin.get_terminals("negative"),
            vin.get_terminals("negative") + DOWN * np.sqrt(8) - (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))),
        )
        circuit.add_wire(
            vin.get_terminals("negative") + DOWN * np.sqrt(8) - (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))),
            vin.get_terminals("negative") + DOWN * np.sqrt(8) - (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))) + RIGHT * 4,
        )

        circuit.add_wire(
            vin.get_terminals("positive"),
            vin.get_terminals("positive") + UP * np.sqrt(8) + (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))),
        )
        circuit.add_wire(
            vin.get_terminals("positive") + UP * np.sqrt(8) + (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))),
            vin.get_terminals("positive") + UP * np.sqrt(8) + (0.5 * (vin.get_terminals("negative") - vin.get_terminals("positive"))) + RIGHT * 4,
        )


        # Animation
        self.play(Create(circuit), run_time=1)
        self.wait(2)