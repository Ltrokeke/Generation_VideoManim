"""
scene1_architecture_overview.py — GLANCE Architecture Overview (Corrected Branching Flowchart).

Layout:
    Box 1 (Router)       — LEFT
    Box 2 (LLM Encoder)  — TOP-RIGHT
    Box 3 (Refiner MLP)  — MIDDLE-RIGHT (below Box 2)
    Box 4 (Final Output) — BOTTOM-RIGHT (flat, wide)

Two paths:
    Route x : Box1 → Box4 directly (skip LLM AND Refiner)
    Route v : Box1 → Box2 → Box3 → Box4

Render:
    manim -pql scenes/scene1_architecture_overview.py Scene1_ArchitectureOverview
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
import numpy as np
from config import *
from utils import *
from components import *


class Scene1_ArchitectureOverview(Scene):

    def construct(self):
        apply_scene_config(self)

        # ============================================================
        # PHASE 1: TITLE
        # ============================================================
        title = Text(
            "GLANCE Architecture Overview",
            font_size=34, color=TEXT_PRIMARY, weight=BOLD,
        )
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 2: CREATE 4 BOXES
        # ============================================================

        # --- BOX 1: Router (LEFT) ---
        b1_rect = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=2.4,
            color=YELLOW, fill_color="#2d2305", fill_opacity=0.88, stroke_width=2.5,
        )
        b1_badge = Text("STEP 1", font_size=11, color=YELLOW, weight=BOLD)
        b1_title = Text("Router", font_size=24, color=TEXT_PRIMARY, weight=BOLD)
        b1_sub = Text("Node-level\nRouting Decision", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b1_content = VGroup(b1_badge, b1_title, b1_sub).arrange(DOWN, buff=0.12)
        b1 = VGroup(b1_rect, b1_content)
        b1.move_to(LEFT * 4.2 + DOWN * 0.3)

        # --- BOX 2: LLM Encoder (TOP-RIGHT) ---
        b2_rect = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=1.6,
            color=BLUE, fill_color="#0d213a", fill_opacity=0.88, stroke_width=2.5,
        )
        b2_badge = Text("STEP 2", font_size=11, color=BLUE_B, weight=BOLD)
        b2_title = Text("LLM Encoder", font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        b2_sub = Text("Multi-layer Embedding", font_size=12, color=TEXT_SECONDARY)
        b2_content = VGroup(b2_badge, b2_title, b2_sub).arrange(DOWN, buff=0.1)
        b2 = VGroup(b2_rect, b2_content)
        b2.move_to(RIGHT * 3.5 + UP * 1.8)

        # --- BOX 3: Refiner MLP (MIDDLE-RIGHT, below Box 2) ---
        b3_rect = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=1.5,
            color=PURPLE, fill_color="#241238", fill_opacity=0.88, stroke_width=2.5,
        )
        b3_badge = Text("STEP 3", font_size=11, color=PURPLE_B, weight=BOLD)
        b3_title = Text("Refiner MLP", font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        b3_sub = Text("Prediction Fusion", font_size=12, color=TEXT_SECONDARY)
        b3_content = VGroup(b3_badge, b3_title, b3_sub).arrange(DOWN, buff=0.1)
        b3 = VGroup(b3_rect, b3_content)
        b3.move_to(RIGHT * 3.5 + DOWN * 0.3)

        # --- BOX 4: Final Output (BOTTOM-RIGHT, flat & wide) ---
        b4_rect = RoundedRectangle(
            corner_radius=0.12, width=5.0, height=1.0,
            color=GRAY, fill_color="#1e293b", fill_opacity=0.85, stroke_width=2.0,
        )
        b4_title = Text("Final Output (GNN Predictions)", font_size=16, color=TEXT_PRIMARY, weight=BOLD)
        b4 = VGroup(b4_rect, b4_title)
        b4.move_to(RIGHT * 2.5 + DOWN * 2.5)

        # --- Frozen badge above Box 2 ---
        frozen_badge_box = RoundedRectangle(
            corner_radius=0.08, width=1.6, height=0.4,
            color="#06b6d4", fill_color="#083344", fill_opacity=0.95, stroke_width=1.5,
        )
        frozen_badge_txt = Text("Frozen", font_size=12, color="#22d3ee", weight=BOLD)
        frozen_badge_txt.move_to(frozen_badge_box.get_center())
        frozen_badge = VGroup(frozen_badge_box, frozen_badge_txt)
        frozen_badge.next_to(b2_rect, UP, buff=0.1)

        # --- FadeIn all 4 boxes + frozen badge ---
        self.play(
            FadeIn(b1, shift=RIGHT * 0.3),
            FadeIn(b2, shift=DOWN * 0.3),
            FadeIn(b3, shift=LEFT * 0.3),
            FadeIn(b4, shift=UP * 0.2),
            FadeIn(frozen_badge, shift=DOWN * 0.2),
            run_time=1.0,
        )
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 3: ROUTE x — Easy Node (Skip LLM AND Refiner)
        # Box 1 → Box 4 directly
        # ============================================================
        easy_label = Text("Easy Node (Not Routed)", font_size=13, color=RED_B)
        easy_label.next_to(b1_rect, DOWN, buff=0.18)

        # Arrow from Box1 right-bottom edge → Box4 left edge
        route_x_start = b1_rect.get_right() + DOWN * 0.6
        route_x_end = b4_rect.get_left() + UP * 0.05
        route_x_arrow = Arrow(
            route_x_start, route_x_end,
            buff=0.1, color=RED, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.12,
        )
        route_x_label = MathTex(
            r"\text{Route}\;\times",
            font_size=24, color=RED,
        )
        route_x_label.next_to(route_x_arrow.point_from_proportion(0.45), DOWN, buff=0.12)

        # Data dot
        dot1 = Dot(radius=0.11, color=WHITE).move_to(b1_rect.get_left() + LEFT * 0.6)
        dot1_path_in = Line(dot1.get_center(), b1_rect.get_center())
        dot1_path_skip = Line(route_x_start, route_x_end)

        # Show easy label
        self.play(FadeIn(easy_label, shift=DOWN * 0.15), run_time=0.5)

        # Dot enters Router
        self.play(
            FadeIn(dot1, scale=0.5),
            MoveAlongPath(dot1, dot1_path_in, rate_func=smooth, run_time=0.7),
        )
        self.play(Indicate(b1_rect, color=YELLOW, scale_factor=1.03), run_time=0.5)
        self.wait(0.2)

        # Draw red arrow + label
        self.play(GrowArrow(route_x_arrow), FadeIn(route_x_label), run_time=0.6)

        # Dot slides along red arrow to Box4
        dot1_slide = dot1.copy().move_to(route_x_start)
        self.add(dot1_slide)
        self.remove(dot1)
        self.play(
            MoveAlongPath(dot1_slide, dot1_path_skip, rate_func=smooth, run_time=1.2),
        )
        self.play(
            Flash(b4_rect.get_center(), color=WHITE, line_length=0.2, num_lines=8, run_time=0.6),
        )
        self.remove(dot1_slide)
        self.play(FadeOut(easy_label), run_time=0.3)
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 4: ROUTE v — Hard Node (Router → LLM → Refiner → Output)
        # Box 1 → Box 2 → Box 3 → Box 4
        # ============================================================
        hard_label = Text("Hard Node (Routed)", font_size=13, color=GREEN_B)
        hard_label.next_to(b1_rect, DOWN, buff=0.18)

        # Arrow 1: Box1 → Box2 (GREEN)
        route_v_start = b1_rect.get_right() + UP * 0.4
        route_v_end = b2_rect.get_left() + DOWN * 0.1
        route_v_arrow = Arrow(
            route_v_start, route_v_end,
            buff=0.1, color=GREEN, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.12,
        )
        route_v_label = MathTex(
            r"\text{Route}\;\checkmark",
            font_size=24, color=GREEN,
        )
        route_v_label.next_to(route_v_arrow.point_from_proportion(0.45), UP, buff=0.12)

        # Arrow 2: Box2 → Box3 (YELLOW)
        llm_to_refiner_arrow = Arrow(
            b2_rect.get_bottom(), b3_rect.get_top(),
            buff=0.1, color=YELLOW, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.15,
        )
        llm_to_refiner_label = Text("Embed", font_size=12, color=YELLOW, weight=BOLD)
        llm_to_refiner_label.next_to(llm_to_refiner_arrow, RIGHT, buff=0.1)

        # Arrow 3: Box3 → Box4 (PURPLE)
        refiner_to_out_arrow = Arrow(
            b3_rect.get_bottom(), b4_rect.get_top() + LEFT * 0.3,
            buff=0.1, color=PURPLE, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.15,
        )
        refiner_to_out_label = Text("Fuse", font_size=12, color=PURPLE_B, weight=BOLD)
        refiner_to_out_label.next_to(refiner_to_out_arrow, RIGHT, buff=0.1)

        # Paths for dot movement
        dot2_path_in = Line(b1_rect.get_left() + LEFT * 0.6, b1_rect.get_center())
        dot2_path_up = Line(route_v_start, route_v_end)
        dot2_path_down1 = Line(b2_rect.get_bottom(), b3_rect.get_top())
        dot2_path_down2 = Line(b3_rect.get_bottom(), b4_rect.get_top() + LEFT * 0.3)

        # Data dot 2
        dot2 = Dot(radius=0.11, color=WHITE).move_to(b1_rect.get_left() + LEFT * 0.6)

        # Show hard label
        self.play(FadeIn(hard_label, shift=DOWN * 0.15), run_time=0.5)

        # Dot enters Router
        self.play(
            FadeIn(dot2, scale=0.5),
            MoveAlongPath(dot2, dot2_path_in, rate_func=smooth, run_time=0.7),
        )
        self.play(Indicate(b1_rect, color=YELLOW, scale_factor=1.03), run_time=0.5)
        self.wait(0.2)

        # Step A: Box1 → Box2 (GREEN arrow)
        self.play(GrowArrow(route_v_arrow), FadeIn(route_v_label), run_time=0.5)
        dot2_a = dot2.copy().move_to(route_v_start)
        self.add(dot2_a)
        self.remove(dot2)
        self.play(
            MoveAlongPath(dot2_a, dot2_path_up, rate_func=smooth, run_time=1.0),
        )
        # LLM reacts
        self.play(
            Indicate(b2_rect, color=BLUE, scale_factor=1.04),
            Wiggle(b2_rect, scale_value=1.02, rotation_angle=0.015 * TAU, n_wiggles=3, run_time=0.7),
        )
        self.wait(0.2)

        # Step B: Box2 → Box3 (YELLOW arrow)
        self.play(GrowArrow(llm_to_refiner_arrow), FadeIn(llm_to_refiner_label), run_time=0.5)
        dot2_b = dot2_a.copy().move_to(b2_rect.get_bottom())
        self.add(dot2_b)
        self.remove(dot2_a)
        self.play(
            MoveAlongPath(dot2_b, dot2_path_down1, rate_func=smooth, run_time=0.7),
        )
        self.play(
            Indicate(b3_rect, color=PURPLE, scale_factor=1.04),
            run_time=0.5,
        )
        self.wait(0.2)

        # Step C: Box3 → Box4 (PURPLE arrow)
        self.play(GrowArrow(refiner_to_out_arrow), FadeIn(refiner_to_out_label), run_time=0.5)
        dot2_c = dot2_b.copy().move_to(b3_rect.get_bottom())
        self.add(dot2_c)
        self.remove(dot2_b)
        self.play(
            MoveAlongPath(dot2_c, dot2_path_down2, rate_func=smooth, run_time=0.7),
        )
        self.play(
            Flash(b4_rect.get_center(), color=PURPLE, line_length=0.25, num_lines=10, run_time=0.8),
            Circumscribe(b4_rect, color=WHITE, stroke_width=2.5, time_width=0.5),
        )
        self.remove(dot2_c)
        self.play(FadeOut(hard_label), run_time=0.3)
        self.wait(WAIT_LONG)
