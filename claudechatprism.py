from manim import *
from manim.utils.color import color_to_rgb, rgb_to_color
import numpy as np

def color_from_hex(hex_str):
    return rgb_to_color(color_to_rgb(hex_str))

def interpolate_roygbiv(colors, alpha):
    n = len(colors) - 1
    seg = alpha * n
    i = int(np.floor(seg))
    frac = seg - i
    if i >= n:
        return colors[-1]
    return interpolate_color(colors[i], colors[i+1], frac)


class LightDispersionThroughPrism(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Text("", font_size=34)
        title.to_edge(UP)
        self.play(Write(title))

        # Pryzmat
        A = [-1, -1, 0]
        B = [ 1, -1, 0]
        C = [ 0,  1, 0]
        prism = Polygon(A, B, C, color=WHITE, fill_opacity=0.1)
        self.play(Create(prism))

        # Punkt wejścia i wyjścia
        entry_point = [-0.7, -0.1, 0]
        exit_point  = [ 0.5, -0.2, 0]

        # Biały promień wchodzący
        light_source = [-3, -0.1, 0]
        incoming = Line(light_source, entry_point, color=WHITE, stroke_width=2)
        self.play(Create(incoming))

        # Biały promień wewnątrz
        inside_line = Line(entry_point, exit_point, color=WHITE, stroke_width=2)
        self.play(Create(inside_line))

        # (Tu POMIJAMY outgoing!)

        # ROYGBIV
        INDIGO = color_from_hex("#4B0082")
        VIOLET = color_from_hex("#9400D3")
        roygbiv = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

        n_lines = 80
        angle_min = -5 * DEGREES
        angle_max = -25 * DEGREES
        beam_length = 4

        # Określmy "podstawowy" kierunek wychodzenia (jakby to był outgoing).
        # Potrzebny, by wzorować się na nim podczas rozchylania wachlarza.
        # Zróbmy np. out_point = [3, -0.2, 0], jak w poprzednim kodzie:
        out_point = [3, -0.2, 0]
        base_dir = np.array(out_point) - np.array(exit_point)

        lines_group = VGroup()
        for i in range(n_lines):
            alpha = i / (n_lines - 1)
            angle = interpolate(angle_min, angle_max, alpha)
            color = interpolate_roygbiv(roygbiv, alpha)

            base_2d = base_dir[:2]
            rot_mat = rotation_matrix(angle)
            dir_2d = np.dot(rot_mat, base_2d)
            dir_2d /= np.linalg.norm(dir_2d)
            end_2d = np.array(exit_point[:2]) + dir_2d * beam_length
            end_pos = [end_2d[0], end_2d[1], 0]

            beam = Line(exit_point, end_pos, color=color, stroke_width=1)
            lines_group.add(beam)

        self.play(
            LaggedStart(*[Create(ln) for ln in lines_group], lag_ratio=0.01),
            run_time=3
        )

        self.wait(2)


def rotation_matrix(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s], [s, c]])






#python -m manim -qk C:\Users\topgu\PycharmProjects\obrazowanie\venv\claudechatprism.py LightDispersionThroughPrism
#python -m manim -pql C:\Users\topgu\PycharmProjects\obrazowanie\venv\claudechatprism.py LightDispersionThroughPrism