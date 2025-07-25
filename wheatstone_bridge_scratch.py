# cd C:\Users\GAYRARD\Documents\GitHub\Gas_Chromatography
# manim -pqm wheatstone_bridge_scratch.py WheatstoneBridge

from manim import *
from manim_chemistry import *

class WheatstoneBridge(Scene):
    def construct(self):
        # distance
        a = 2
        r_width = 1
        r_height = 0.5

        # Résistances
        r1 = Rectangle(width=r_width, height=r_height).shift(UP * a)
        r2 = Rectangle(width=r_width, height=r_height).shift(RIGHT * a).rotate(90 * DEGREES)
        r3 = Rectangle(width=r_width, height=r_height).shift(DOWN * a)
        r4 = Rectangle(width=r_width, height=r_height).shift(LEFT * a).rotate(90 * DEGREES)

        # Labels des résistances
        label_r1 = Tex(r"$R_{1}$").scale(0.6).next_to(r1, UP)
        label_r2 = Tex(r"$R_{2}$").scale(0.6).next_to(r2, RIGHT)
        label_r3 = Tex(r"$R_{3}$").scale(0.6).next_to(r3, DOWN)
        label_r4 = Tex(r"$R_{4}$").scale(0.6).next_to(r4, LEFT)

        # Nœuds d'angle droit
        n12 = np.array([r2.get_top()[0], r1.get_right()[1], 0])
        n23 = np.array([r2.get_bottom()[0], r3.get_right()[1], 0])
        n34 = np.array([r4.get_bottom()[0], r3.get_left()[1], 0])
        n41 = np.array([r4.get_top()[0], r1.get_left()[1], 0])

        # Câbles du carré
        c1 = VGroup(
            Line(start=r1.get_right(), end=n12),
            Line(start=n12, end=r2.get_top())
        )
        c2 = VGroup(
            Line(start=r2.get_bottom(), end=n23),
            Line(start=n23, end=r3.get_right())
        )
        c3 = VGroup(
            Line(start=r3.get_left(), end=n34),
            Line(start=n34, end=r4.get_bottom())
        )
        c4 = VGroup(
            Line(start=r4.get_top(), end=n41),
            Line(start=n41, end=r1.get_left())
        )

        # Nœuds virtuels
        dot_n12 = Dot(n12, radius=0.01, color=BLACK, fill_opacity=0.0)
        dot_n34 = Dot(n34, radius=0.01, color=BLACK, fill_opacity=0.0)
        dot_n41 = Dot(n41, radius=0.01, color=BLACK, fill_opacity=0.0)
        dot_n23 = Dot(n23, radius=0.01, color=BLACK, fill_opacity=0.0)

        # Circuit initial
        circuit = VGroup(r1, c1, r2, c2, r3, c3, r4, c4, dot_n12, dot_n34, dot_n41, dot_n23,
                         label_r1, label_r2, label_r3, label_r4)

        self.play(Create(circuit), run_time=3)
        self.play(
            Rotate(circuit, angle=45 * DEGREES, about_point=ORIGIN, run_time=1)
            )
        for label in [label_r1, label_r2, label_r3, label_r4]:
            self.play(
                Rotate(label, angle=-45 * DEGREES, about_point=label.get_center(), run_time=0.3)
            )

        self.play(circuit.animate.shift(RIGHT * a/2), run_time=1.5)

        # Ajout de la source Vin
        vin = Circle(radius=0.5, color=WHITE).shift(LEFT * a * 1.5)
        plus_sign = Cross(scale_factor=0.07, stroke_color=WHITE, stroke_width=4).move_to(vin.get_center()+UP*0.2).rotate(45 * DEGREES)
        minus_sign = Line(start=vin.get_center()+DOWN*0.2 + LEFT*0.1, end=vin.get_center()+DOWN*0.2 + RIGHT*0.1)

        label_vin = Tex(r"$V_{in}$", color=WHITE).next_to(vin, LEFT).scale(0.6)

        self.play(Create(vin), Create(plus_sign), Create(minus_sign), Create(label_vin), run_time=1)

        # Mise à jour des coordonnées
        n12_final = dot_n12.get_center()
        n34_final = dot_n34.get_center()
        n41_final = dot_n41.get_center()
        n23_final = dot_n23.get_center()

        # Câbles Vin
        start_plus = vin.get_top()
        corner_vin1 = np.array([start_plus[0], n12_final[1], 0])
        c_vin1 = VGroup(
            Line(start=start_plus, end=corner_vin1, color=WHITE),
            Line(start=corner_vin1, end=n12_final, color=WHITE)
        )

        start_minus = vin.get_bottom()
        corner_vin2 = np.array([start_minus[0], n34_final[1], 0])
        c_vin2 = VGroup(
            Line(start=start_minus, end=corner_vin2, color=WHITE),
            Line(start=corner_vin2, end=n34_final, color=WHITE)
        )

        # Vout
        c_measure1 = Line(start=n41_final, end=n41_final + RIGHT * a)
        c_measure2 = Line(start=n23_final, end=n23_final + LEFT * a)
        dot_measure1 = Dot(c_measure1.get_end(), radius=0.05, fill_opacity=1.0)
        dot_measure2 = Dot(c_measure2.get_end(), radius=0.05, fill_opacity=1.0)

        label_vout = Tex(r"$V_{out}$").scale(0.6)
        label_vout.move_to((dot_measure1.get_center() + dot_measure2.get_center()) / 2)

        c_measure = VGroup(c_measure1, c_measure2, dot_measure1, dot_measure2)

        self.play(Create(c_vin1), Create(c_vin2), Create(c_measure), Create(label_vout), run_time=1.5)

        self.wait(1)
        circuit.add(c_vin1, c_vin2, c_measure)
        
        # Créer la lampe à la place de R2
        lamp = VGroup(
            Circle(radius=r_width/2, color=WHITE),
            Cross(scale_factor=0.35, stroke_color=WHITE, stroke_width=3)
        ).move_to(r2.get_center())

        # Remplacer R2 par la lampe
        self.play(FadeOut(label_r2), Transform(r2, lamp), run_time=1.5)

        # Récupère le centre de la lampe
        lamp_center = lamp.get_center()

        # Rayon estimé (en supposant que lamp_shape est un cercle ou forme circulaire)
        lamp_radius = lamp[0].width / 2  # lamp[0] est la forme, pas le label

        # Vecteurs directionnels à ±45°
        vec_45 = rotate_vector(RIGHT, -45 * DEGREES)
        vec_minus_45 = rotate_vector(LEFT, -45 * DEGREES)

        # Points de contact sur la lampe à ±45° autour de son centre
        contact_entry = lamp_center + vec_minus_45 * lamp_radius
        contact_exit = lamp_center + vec_45 * lamp_radius

        # Points d'entrée et de sortie invisibles
        line_dots = VGroup(
            Dot(LEFT * 0.5, radius=0.05, fill_opacity=0),   # point d'entrée (en haut à gauche)
            Dot(RIGHT * 0.5, radius=0.05, fill_opacity=0),  # point de sortie (en haut à droite)
        ).shift(UP * a * 2).rotate(-45 * DEGREES, about_point=ORIGIN).shift(RIGHT * a / 2)

        # Créer le chemin comme une seule ligne continue
        # Ordre corrigé : entrée -> gauche lampe -> droite lampe -> sortie
        path_points = [
            line_dots[0].get_center(),  # point d'entrée (haut gauche)
            contact_entry,              # côté gauche de la lampe
            contact_exit,               # côté droit de la lampe
            line_dots[1].get_center()   # point de sortie (haut droite)
        ]
        
        # Créer un VMobject pour le chemin
        path = VMobject()
        path.set_points_as_corners(path_points)
        
        # Lignes de trajectoire pour la visualisation
        line_path = VGroup(
            Line(start=line_dots[0].get_center(), end=contact_entry, color=BLUE, stroke_width=2),
            Line(start=contact_entry, end=contact_exit, color=BLUE, stroke_width=2),
            Line(start=contact_exit, end=line_dots[1].get_center(), color=BLUE, stroke_width=2)
        ).set_opacity(1)

        # Affichage du chemin
        self.add(line_path)
        self.wait(1)

        # Créer et animer la molécule
        graph_molecule = GraphMolecule.molecule_from_file("molecules\\butane_2d.mol", ignore_hydrogens=False).scale(0.3)
        
        # Positionner la molécule au début du chemin
        graph_molecule.move_to(line_dots[0].get_center())
        
        # Ajouter la molécule à la scène
        self.add(graph_molecule)
        
        # Animer la molécule le long du chemin
        self.play(
            MoveAlongPath(graph_molecule, path), 
            run_time=3, 
            rate_func=smooth
        )

        self.wait(2)