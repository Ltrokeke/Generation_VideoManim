"""
scene1_architecture_overview.py — GLANCE Architecture Overview (Branching Flowchart).

Two data paths:
  Route ×  : Easy nodes skip LLM → straight to Refiner
  Route ✓  : Hard nodes go Router → LLM Encoder → Refiner

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
    """
    GLANCE Architecture Overview — Branching Flowchart
    Route × : Easy nodes skip LLM → go straight to Refiner
    Route ✓ : Hard nodes go Router → LLM → Refiner
    """

    def construct(self):
        apply_scene_config(self)

        # ============================================================
        # PHASE 1: TITLE
        # ============================================================
        title = Text(
            "GLANCE Architecture Overview",
            font_size=34, color=TEXT_PRIMARY, weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 2: CREATE 3 BOXES
        # ============================================================
        BOX_W, BOX_H = 3.6, 1.8

        # --- BOX 1: Router (Left, Yellow border) ---
        b1_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=YELLOW, fill_color="#2d2305", fill_opacity=0.88, stroke_width=2.5,
        )
        b1_badge = Text("STEP 1", font_size=11, color=YELLOW, weight=BOLD)
        b1_title = Text("Router", font_size=24, color=TEXT_PRIMARY, weight=BOLD)
        b1_sub = Text("Node-level Routing\nDecision", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b1_content = VGroup(b1_badge, b1_title, b1_sub).arrange(DOWN, buff=0.1)
        b1 = VGroup(b1_rect, b1_content)
        b1.move_to(LEFT * 4.0 + DOWN * 0.4)

        # --- BOX 2: LLM Encoder (Top-Right, Blue border) ---
        b2_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=BLUE, fill_color="#0d213a", fill_opacity=0.88, stroke_width=2.5,
        )
        b2_badge = Text("STEP 2", font_size=11, color=BLUE_B, weight=BOLD)
        b2_title = Text("LLM Encoder", font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        b2_sub = Text("Multi-layer\nEmbedding", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b2_content = VGroup(b2_badge, b2_title, b2_sub).arrange(DOWN, buff=0.1)
        b2 = VGroup(b2_rect, b2_content)
        b2.move_to(RIGHT * 3.0 + UP * 1.2)

        # --- BOX 3: Refiner & Final Output (Bottom-Right, Purple border) ---
        b3_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=PURPLE, fill_color="#241238", fill_opacity=0.88, stroke_width=2.5,
        )
        b3_badge = Text("STEP 3", font_size=11, color=PURPLE_B, weight=BOLD)
        b3_title = Text("Refiner", font_size=24, color=TEXT_PRIMARY, weight=BOLD)
        b3_sub = Text("Fusion &\nFinal Output", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b3_content = VGroup(b3_badge, b3_title, b3_sub).arrange(DOWN, buff=0.1)
        b3 = VGroup(b3_rect, b3_content)
        b3.move_to(RIGHT * 3.0 + DOWN * 2.0)

        # --- FadeIn all 3 boxes ---
        self.play(
            FadeIn(b1, shift=RIGHT * 0.3),
            FadeIn(b2, shift=DOWN * 0.3),
            FadeIn(b3, shift=UP * 0.3),
            run_time=0.9,
        )
        self.wait(0.3)

        # ============================================================
        # PHASE 3: FROZEN BADGE on LLM + TRAINABLE highlight
        # ============================================================
        frozen_badge_box = RoundedRectangle(
            corner_radius=0.08, width=1.8, height=0.42,
            color="#06b6d4", fill_color="#083344", fill_opacity=0.95, stroke_width=1.5,
        )
        frozen_badge_txt = Text("Frozen", font_size=13, color="#22d3ee", weight=BOLD)
        frozen_badge_txt.move_to(frozen_badge_box.get_center())
        frozen_badge = VGroup(frozen_badge_box, frozen_badge_txt)
        frozen_badge.next_to(b2_rect, UP, buff=0.12)
        frozen_badge.shift(UP * 1.0)

        self.play(
            frozen_badge.animate.shift(DOWN * 1.0),
            run_time=0.7,
        )
        self.wait(0.3)

        # Trainable modules highlight
        trainable_txt = Text(
            "Trainable Modules",
            font_size=14, color=YELLOW, weight=BOLD,
        )
        trainable_txt.to_edge(DOWN, buff=0.45)

        self.play(
            Circumscribe(b1_rect, color=YELLOW, stroke_width=3.5, time_width=0.5),
            Circumscribe(b3_rect, color=YELLOW, stroke_width=3.5, time_width=0.5),
            FadeIn(trainable_txt, shift=UP * 0.2),
            run_time=1.2,
        )
        self.wait(1.5)
        self.play(FadeOut(trainable_txt), run_time=0.4)
        self.wait(0.3)

        # ============================================================
        # PHASE 4: ROUTE × — Easy Node (Skip LLM)
        # ============================================================
        route_skip_arrow = Arrow(
            b1_rect.get_right() + DOWN * 0.3,
            b3_rect.get_left() + UP * 0.1,
            buff=0.12, color=RED, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.18,
        )
        route_skip_label = MathTex(
            r"\text{Route} \times",
            font_size=22, color=RED,
        )
        route_skip_label.next_to(route_skip_arrow, DOWN, buff=0.1)

        easy_label = Text("Easy Node (Not Routed)", font_size=12, color=RED_B)
        easy_label.next_to(b1_rect, DOWN, buff=0.15)

        dot1 = Dot(radius=0.1, color=WHITE).move_to(b1_rect.get_left() + LEFT * 0.5)
        dot1_path_in = Line(dot1.get_center(), b1_rect.get_center())
        dot1_path_skip = Line(b1_rect.get_right() + DOWN * 0.3, b3_rect.get_left() + UP * 0.1)

        self.play(
            FadeIn(dot1, scale=0.5),
            MoveAlongPath(dot1, dot1_path_in, rate_func=smooth, run_time=0.6),
        )
        self.play(
            FadeIn(easy_label, shift=DOWN * 0.15),
            Indicate(b1_rect, color=YELLOW, scale_factor=1.03),
            run_time=0.6,
        )
        self.wait(0.3)

        self.play(GrowArrow(route_skip_arrow), FadeIn(route_skip_label), run_time=0.5)

        dot1_skip = dot1.copy().move_to(route_skip_arrow.get_start())
        self.add(dot1_skip)
        self.remove(dot1)

        self.play(
            MoveAlongPath(dot1_skip, dot1_path_skip, rate_func=smooth, run_time=1.0),
        )
        self.play(
            Flash(b3_rect.get_center(), color=PURPLE, line_length=0.2, num_lines=8, run_time=0.6),
        )
        self.remove(dot1_skip)
        self.play(FadeOut(easy_label), run_time=0.3)
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 5: ROUTE ✓ — Hard Node (Go through LLM)
        # ============================================================
        route_llm_arrow = Arrow(
            b1_rect.get_right() + UP * 0.3,
            b2_rect.get_left() + DOWN * 0.1,
            buff=0.12, color=GREEN, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.18,
        )
        route_llm_label = MathTex(
            r"\text{Route} \checkmark",
            font_size=22, color=GREEN,
        )
        route_llm_label.next_to(route_llm_arrow, UP, buff=0.1)

        refine_arrow = Arrow(
            b2_rect.get_bottom(),
            b3_rect.get_top(),
            buff=0.12, color=YELLOW, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.18,
        )
        refine_label = Text("Fuse", font_size=13, color=YELLOW, weight=BOLD)
        refine_label.next_to(refine_arrow, RIGHT, buff=0.12)

        hard_label = Text("Hard Node (Routed)", font_size=12, color=GREEN_B)
        hard_label.next_to(b1_rect, DOWN, buff=0.15)

        dot2 = Dot(radius=0.1, color=WHITE).move_to(b1_rect.get_left() + LEFT * 0.5)
        dot2_path_in = Line(dot2.get_center(), b1_rect.get_center())
        dot2_path_up = Line(b1_rect.get_right() + UP * 0.3, b2_rect.get_left() + DOWN * 0.1)
        dot2_path_down = Line(b2_rect.get_bottom(), b3_rect.get_top())

        self.play(
            FadeIn(dot2, scale=0.5),
            MoveAlongPath(dot2, dot2_path_in, rate_func=smooth, run_time=0.6),
        )
        self.play(
            FadeIn(hard_label, shift=DOWN * 0.15),
            Indicate(b1_rect, color=YELLOW, scale_factor=1.03),
            run_time=0.6,
        )
        self.wait(0.3)

        self.play(GrowArrow(route_llm_arrow), FadeIn(route_llm_label), run_time=0.5)

        dot2_up = dot2.copy().move_to(route_llm_arrow.get_start())
        self.add(dot2_up)
        self.remove(dot2)

        self.play(
            MoveAlongPath(dot2_up, dot2_path_up, rate_func=smooth, run_time=1.0),
        )

        self.play(
            Indicate(b2_rect, color=BLUE, scale_factor=1.05),
            Wiggle(b2_rect, scale_value=1.02, rotation_angle=0.02 * TAU, n_wiggles=3, run_time=0.8),
        )
        self.wait(0.3)

        self.play(GrowArrow(refine_arrow), FadeIn(refine_label), run_time=0.5)

        dot2_down = dot2_up.copy().move_to(refine_arrow.get_start())
        self.add(dot2_down)
        self.remove(dot2_up)

        self.play(
            MoveAlongPath(dot2_down, dot2_path_down, rate_func=smooth, run_time=0.8),
        )
        self.play(
            Flash(b3_rect.get_center(), color=PURPLE, line_length=0.25, num_lines=10, run_time=0.8),
            Circumscribe(b3_rect, color=PURPLE, stroke_width=3, time_width=0.5),
        )
        self.remove(dot2_down)
        self.play(FadeOut(hard_label), run_time=0.3)
        self.wait(WAIT_LONG)
