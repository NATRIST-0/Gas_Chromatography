
# cd C:\Users\GAYRARD\Desktop\Python\GC_TCD
# manim -pqm wheatstone_bridge_manim_eng.py WheatstoneBridge

from manim import *
from manim_eng import *

class WheatstoneBridge(Scene):
    def construct(self):
        # Composants du pont
        a = 2

        # Résistances
        r1 = Resistor().set_label("R_1").move_to(UP * a)
        r2 = Resistor().set_label("R_2").move_to(RIGHT * a).rotate(-90 * DEGREES)
        r3 = Resistor().set_label("R_3").move_to(DOWN * a)
        r4 = Resistor().set_label("R_4").move_to(LEFT * a).rotate(-90 * DEGREES)
        
        # Nœuds aux coins du carré (points de jonction)
        corner_top_right = Node().move_to(UP * a + RIGHT * a)
        corner_bottom_right = Node().move_to(DOWN * a + RIGHT * a)
        corner_bottom_left = Node().move_to(DOWN * a + LEFT * a)
        corner_top_left = Node().move_to(UP * a + LEFT * a)
        
        # Création du circuit avec tous les composants
        circuit = Circuit(
            r1, r2, r3, r4, 
            corner_top_right, corner_bottom_right, corner_bottom_left, corner_top_left
        )

        # Animation de création
        self.play(Create(circuit))

        # Connexions animées - structure du pont
        self.play(
            # Connexion R1 au coin supérieur droit
            circuit.animate.connect(r1.right, corner_top_right.left),
            # Connexion coin supérieur droit à R2
            circuit.animate.connect(corner_top_right.down, r2.left),
            # Connexion R2 au coin inférieur droit
            circuit.animate.connect(r2.right, corner_bottom_right.up),
            # Connexion coin inférieur droit à R3
            circuit.animate.connect(corner_bottom_right.left, r3.right),
            # Connexion R3 au coin inférieur gauche
            circuit.animate.connect(r3.left, corner_bottom_left.right),
            # Connexion coin inférieur gauche à R4
            circuit.animate.connect(corner_bottom_left.up, r4.right),
            # Connexion R4 au coin supérieur gauche
            circuit.animate.connect(r4.left, corner_top_left.down),
            # Fermeture du circuit - coin supérieur gauche à R1
            circuit.animate.connect(corner_top_left.right, r1.left),
        )

        # Rotation du circuit - maintenant les connexions suivront correctement
        circuit.rotate(45 * DEGREES)
        self.play(Create(circuit))
        self.wait(2)
