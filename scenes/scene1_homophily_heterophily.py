"""
Scene 1: Homophily vs Heterophily
- Why GNN is strong/weak depending on graph structure
- Local Homophily formula
- Dynamic Message Passing animation on both graphs

Render:
    manim -pql scenes/scene1_homophily_heterophily.py Scene1_HomophilyHeterophily
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
import numpy as np
from config import *
from utils import *
from components import *


class Scene1_HomophilyHeterophily(Scene):

    def construct(self):
        apply_scene_config(self)

        # ============================================================
        # PHASE 1: TITLE & FORMULA
        # ============================================================
        title = Text(
            "Local Homophily",
            font_size=36,
            color=TEXT_PRIMARY,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)

        formula = MathTex(
            r"h_v",
            r"=",
            r"\frac{1}{|\mathcal{N}(v)|}",
            r"\sum_{u \in \mathcal{N}(v)}",
            r"\mathbf{1}[y_u = y_v]",
            font_size=40,
        )
        formula.next_to(title, DOWN, buff=0.35)

        # --- Show Title ---
        self.play(fade_in_shift(title, direction=DOWN), run_time=0.8)
        self.wait(WAIT_SHORT)

        # --- Write Formula ---
        self.play(Write(formula), run_time=2.0)
        self.wait(WAIT_LONG)

        # --- Move & scale formula to top-left corner (clearly readable) ---
        title_formula = VGroup(title, formula)
        self.play(
            title_formula.animate.scale(0.72).to_corner(UL, buff=0.45),
            run_time=ANIM_SPEED_NORMAL,
        )
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 2: BUILD TWO GRAPHS (Left & Right)
        # ============================================================

        CENTER_R = 0.38          # Radius for center node
        NEIGHBOR_R = 0.28        # Radius for neighbor nodes
        ORBIT = 1.55             # Distance neighbor -> center
        GRAPH_Y = -0.35          # Vertical center of graph

        # ==========================
        # LEFT GRAPH: HOMOPHILY
        # ==========================
        left_pos = np.array([-3.3, GRAPH_Y, 0])

        l_center = Circle(
            radius=CENTER_R, color=GREEN,
            fill_color=GREEN_E, fill_opacity=0.9, stroke_width=3,
        ).move_to(left_pos)
        l_center_v = Text("v", font_size=20, color=WHITE, weight=BOLD)
        l_center_v.move_to(left_pos)

        # 4 neighbors (all GREEN) - 45°, 135°, 225°, 315°
        l_angles = [PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4]
        l_neighbors = []
        l_edges = []

        for angle in l_angles:
            pos = left_pos + np.array([
                np.cos(angle), np.sin(angle), 0
            ]) * ORBIT

            node = Circle(
                radius=NEIGHBOR_R, color=GREEN,
                fill_color=GREEN_D, fill_opacity=0.75, stroke_width=2.5,
            ).move_to(pos)
            l_neighbors.append(node)

            edge = Line(
                left_pos, pos,
                color=EDGE_COLOR, stroke_width=3,
            )
            l_edges.append(edge)

        l_label = Text(
            "Homophily: GNN Strong",
            font_size=22, color=GREEN, weight=BOLD,
        )
        l_all_nodes = VGroup(l_center, *l_neighbors)
        l_label.next_to(l_all_nodes, DOWN, buff=0.45)

        # ==========================
        # RIGHT GRAPH: HETEROPHILY
        # ==========================
        right_pos = np.array([3.3, GRAPH_Y, 0])

        r_center = Circle(
            radius=CENTER_R, color=GREEN,
            fill_color=GREEN_E, fill_opacity=0.9, stroke_width=3,
        ).move_to(right_pos)
        r_center_v = Text("v", font_size=20, color=WHITE, weight=BOLD)
        r_center_v.move_to(right_pos)

        # 3 neighbors: RED, YELLOW, PURPLE - 90°, 210°, 330°
        r_colors = [RED, YELLOW, PURPLE]
        r_fill_colors = [RED_E, YELLOW_E, PURPLE_E]
        r_angles = [PI / 2, 7 * PI / 6, 11 * PI / 6]
        r_neighbors = []
        r_edges = []

        for angle, nc, fc in zip(r_angles, r_colors, r_fill_colors):
            pos = right_pos + np.array([
                np.cos(angle), np.sin(angle), 0
            ]) * ORBIT

            node = Circle(
                radius=NEIGHBOR_R, color=nc,
                fill_color=fc, fill_opacity=0.75, stroke_width=2.5,
            ).move_to(pos)
            r_neighbors.append(node)

            edge = Line(
                right_pos, pos,
                color=EDGE_COLOR, stroke_width=3,
            )
            r_edges.append(edge)

        r_label = Text(
            "Heterophily: GNN Weak",
            font_size=22, color=RED, weight=BOLD,
        )
        r_all_nodes = VGroup(r_center, *r_neighbors)
        r_label.next_to(r_all_nodes, DOWN, buff=0.45)

        # --- Divider line between graphs ---
        divider = DashedLine(
            UP * 3, DOWN * 3.5,
            color=TEXT_MUTED, stroke_width=1.5, dash_length=0.15,
        )

        # ==========================
        # ANIMATE: Create Graphs
        # ==========================
        self.play(Create(divider), run_time=0.4)

        self.play(
            *[Create(e) for e in l_edges + r_edges],
            run_time=ANIM_SPEED_NORMAL,
        )

        all_nodes = [l_center] + l_neighbors + [r_center] + r_neighbors
        self.play(
            *[GrowFromCenter(n) for n in all_nodes],
            run_time=ANIM_SPEED_NORMAL,
        )

        self.play(
            FadeIn(l_center_v, scale=0.5),
            FadeIn(r_center_v, scale=0.5),
            run_time=0.4,
        )

        self.play(
            fade_in_shift(l_label, direction=UP, shift_distance=0.3),
            fade_in_shift(r_label, direction=UP, shift_distance=0.3),
        )
        self.wait(WAIT_LONG)

        # ============================================================
        # PHASE 3: ENHANCED DYNAMIC MOTION & MESSAGE PASSING
        # ============================================================

        # Step 1: Pulse / Highlight neighbor nodes (Feature readiness)
        self.play(
            *[
                Indicate(n, scale_factor=1.2, color=n.get_color())
                for n in l_neighbors + r_neighbors
            ],
            run_time=0.8,
        )
        self.wait(0.2)

        # Step 2: Multi-packet data stream moving along edges from neighbors to center
        DOT_R = 0.09

        # Wave 1: First batch of message particles
        wave1_l_dots = [
            Dot(radius=DOT_R, color=GREEN_B, fill_opacity=1).move_to(nb.get_center())
            for nb in l_neighbors
        ]
        wave1_r_dots = [
            Dot(radius=DOT_R, color=nc, fill_opacity=1).move_to(nb.get_center())
            for nb, nc in zip(r_neighbors, r_colors)
        ]

        # Wave 2: Second trailing batch for fluid streaming effect
        wave2_l_dots = [
            Dot(radius=DOT_R * 0.8, color=GREEN_A, fill_opacity=0.85).move_to(nb.get_center())
            for nb in l_neighbors
        ]
        wave2_r_dots = [
            Dot(radius=DOT_R * 0.8, color=nc, fill_opacity=0.85).move_to(nb.get_center())
            for nb, nc in zip(r_neighbors, r_colors)
        ]

        # Edge flashing effect to show active data transfer channels
        l_flash_edges = [
            Line(nb.get_center(), l_center.get_center(), color=GREEN_B, stroke_width=4.5)
            for nb in l_neighbors
        ]
        r_flash_edges = [
            Line(nb.get_center(), r_center.get_center(), color=nc, stroke_width=4.5)
            for nb, nc in zip(r_neighbors, r_colors)
        ]

        # Spawn wave 1 particles + edge glowing pulses
        self.play(
            *[FadeIn(d, scale=0.4) for d in wave1_l_dots + wave1_r_dots],
            *[ShowPassingFlash(e, time_width=0.4, run_time=1.4) for e in l_flash_edges + r_flash_edges],
            *[
                MoveAlongPath(
                    dot,
                    Line(dot.get_center(), l_center.get_center()),
                    rate_func=smooth,
                    run_time=1.4,
                )
                for dot in wave1_l_dots
            ],
            *[
                MoveAlongPath(
                    dot,
                    Line(dot.get_center(), r_center.get_center()),
                    rate_func=smooth,
                    run_time=1.4,
                )
                for dot in wave1_r_dots
            ],
        )

        # Wave 2 stream follows immediately
        self.play(
            *[FadeIn(d, scale=0.4) for d in wave2_l_dots + wave2_r_dots],
            *[
                MoveAlongPath(
                    dot,
                    Line(dot.get_center(), l_center.get_center()),
                    rate_func=smooth,
                    run_time=1.1,
                )
                for dot in wave2_l_dots
            ],
            *[
                MoveAlongPath(
                    dot,
                    Line(dot.get_center(), r_center.get_center()),
                    rate_func=smooth,
                    run_time=1.1,
                )
                for dot in wave2_r_dots
            ],
        )

        # Clean up stream dots
        self.remove(*wave1_l_dots, *wave1_r_dots, *wave2_l_dots, *wave2_r_dots)

        # Step 3: Center nodes reaction to aggregated messages
        # - Left (Homophily): Harmonic resonance, expanding green flash ring (Information aligned)
        # - Right (Heterophily): Conflicting signal collision, warning wobble & noise flash
        self.play(
            Circumscribe(
                l_center, color=GREEN_A, stroke_width=4,
                fade_out=True, run_time=1.5,
            ),
            Flash(l_center, color=GREEN_B, line_length=0.25, num_lines=10, run_time=1.2),
            l_center.animate.set_stroke(color=GREEN_A, width=4.5),
            Wiggle(
                r_center, scale_value=1.3,
                rotation_angle=0.08 * TAU, n_wiggles=6, run_time=1.5,
            ),
            Flash(r_center, color=RED_B, line_length=0.2, num_lines=8, run_time=1.2),
            r_center.animate.set_stroke(color=RED_B, width=4.5),
        )
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 4: SHOW h_v VALUES & BADGES
        # ============================================================
        hv_left = MathTex(r"h_v \to 1", font_size=32, color=GREEN)
        hv_left.next_to(l_label, DOWN, buff=0.3)

        hv_right = MathTex(r"h_v \to 0", font_size=32, color=RED)
        hv_right.next_to(r_label, DOWN, buff=0.3)

        # Subtle highlight box around result
        hv_left_box = SurroundingRectangle(
            hv_left, color=GREEN, buff=0.15, stroke_width=1.5, corner_radius=0.1
        )
        hv_right_box = SurroundingRectangle(
            hv_right, color=RED, buff=0.15, stroke_width=1.5, corner_radius=0.1
        )

        self.play(
            FadeIn(hv_left, shift=UP * 0.2),
            Create(hv_left_box),
            FadeIn(hv_right, shift=UP * 0.2),
            Create(hv_right_box),
            run_time=0.9,
        )
        self.wait(WAIT_EXTRA_LONG)
