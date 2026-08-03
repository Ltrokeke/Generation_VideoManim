"""
scene1_architecture_overview.py — Scene 1: GLANCE Architecture Overview (Node-aware Fusion).

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
    Sơ đồ hệ thống GLANCE (Figure 2 - Node-aware Fusion).
    - Mục tiêu: Tích hợp GNN và LLM nhận thức theo node, cân bằng hiệu năng và chi phí.
    - Nguyên tắc: Đóng băng (Freeze) GNN & LLM. Chỉ huấn luyện Router & Refiner.
    - 3 Bước: (1) Router -> (2) LLM Embedding -> (3) Refiner (Fusion).
    """

    def construct(self):
        apply_scene_config(self)

        # ============================================================
        # PHASE 1: TITLE & SUBTITLE
        # ============================================================
        title = Text(
            "GLANCE Architecture (Node-aware Fusion)",
            font_size=32,
            color=TEXT_PRIMARY,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)

        subtitle = Text(
            "Efficiency & Node-aware Adaptive Integration",
            font_size=15,
            color=TEXT_SECONDARY,
        )
        subtitle.next_to(title, DOWN, buff=0.12)

        title_group = VGroup(title, subtitle)
        self.play(FadeIn(title_group, shift=DOWN * 0.3), run_time=0.8)
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 2: 3 MAIN PIPELINE BOXES (Router, LLM, Refiner)
        # ============================================================
        BOX_W, BOX_H = 3.3, 2.05
        BOX_Y = -0.35

        # --- BOX 1: Step 1: Router (Green) ---
        b1_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=GREEN, fill_color="#0f2d1e", fill_opacity=0.9, stroke_width=2.5,
        )
        b1_badge = Text("STEP 1", font_size=11, color=GREEN_B, weight=BOLD)
        b1_title = Text("Router", font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        b1_sub = Text("Feature Extraction\n& Node Routing", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b1_content = VGroup(b1_badge, b1_title, b1_sub).arrange(DOWN, buff=0.12)
        b1 = VGroup(b1_rect, b1_content).move_to(LEFT * 4.3 + UP * BOX_Y)

        # --- BOX 2: Step 2: LLM Embedding (Blue) ---
        b2_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=BLUE, fill_color="#0d213a", fill_opacity=0.9, stroke_width=2.5,
        )
        b2_badge = Text("STEP 2", font_size=11, color=BLUE_B, weight=BOLD)
        b2_title = Text("LLM Embedding", font_size=20, color=TEXT_PRIMARY, weight=BOLD)
        b2_sub = Text("Multi-layer Layer\nRepresentations", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b2_content = VGroup(b2_badge, b2_title, b2_sub).arrange(DOWN, buff=0.12)
        b2 = VGroup(b2_rect, b2_content).move_to(UP * BOX_Y)

        # --- BOX 3: Step 3: Refiner (Purple) ---
        b3_rect = RoundedRectangle(
            corner_radius=0.15, width=BOX_W, height=BOX_H,
            color=PURPLE, fill_color="#241238", fill_opacity=0.9, stroke_width=2.5,
        )
        b3_badge = Text("STEP 3", font_size=11, color=PURPLE_B, weight=BOLD)
        b3_title = Text("Refiner", font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        b3_sub = Text("Prediction Fusion\n& Knowledge Mix", font_size=13, color=TEXT_SECONDARY, line_spacing=0.8)
        b3_content = VGroup(b3_badge, b3_title, b3_sub).arrange(DOWN, buff=0.12)
        b3 = VGroup(b3_rect, b3_content).move_to(RIGHT * 4.3 + UP * BOX_Y)

        # --- Connecting Arrows ---
        arrow1 = Arrow(
            b1_rect.get_right(), b2_rect.get_left(),
            buff=0.12, color="#64748b", stroke_width=3.5, max_tip_length_to_length_ratio=0.28,
        )
        arrow2 = Arrow(
            b2_rect.get_right(), b3_rect.get_left(),
            buff=0.12, color="#64748b", stroke_width=3.5, max_tip_length_to_length_ratio=0.28,
        )

        # Sequential animation
        self.play(Create(b1_rect), FadeIn(b1_content, shift=UP * 0.2), run_time=0.7)
        self.play(GrowArrow(arrow1), run_time=0.4)
        self.play(Create(b2_rect), FadeIn(b2_content, shift=UP * 0.2), run_time=0.7)
        self.play(GrowArrow(arrow2), run_time=0.4)
        self.play(Create(b3_rect), FadeIn(b3_content, shift=UP * 0.2), run_time=0.7)
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 3: FROZEN BACKBONES (GNN & LLM)
        # ============================================================
        frozen_llm_badge = VGroup(
            RoundedRectangle(
                corner_radius=0.1, width=2.4, height=0.55,
                color="#06b6d4", fill_color="#083344", fill_opacity=0.95, stroke_width=1.5,
            ),
            Text("❄ Frozen LLM", font_size=13, color="#22d3ee", weight=BOLD),
        )
        frozen_llm_badge[1].move_to(frozen_llm_badge[0].get_center())
        frozen_llm_badge.next_to(b2_rect, UP, buff=0.25)

        frozen_gnn_badge = VGroup(
            RoundedRectangle(
                corner_radius=0.1, width=2.4, height=0.55,
                color="#06b6d4", fill_color="#083344", fill_opacity=0.95, stroke_width=1.5,
            ),
            Text("❄ Frozen GNN", font_size=13, color="#22d3ee", weight=BOLD),
        )
        frozen_gnn_badge[1].move_to(frozen_gnn_badge[0].get_center())
        frozen_gnn_badge.move_to(frozen_llm_badge.get_center() + UP * 0.7)

        frozen_label = Text("Frozen Backbones (Zero Gradient Update)", font_size=14, color="#06b6d4", weight=SEMIBOLD)
        frozen_label.next_to(frozen_gnn_badge, UP, buff=0.18)

        self.play(
            FadeIn(frozen_gnn_badge, shift=DOWN * 0.3),
            FadeIn(frozen_llm_badge, shift=DOWN * 0.3),
            FadeIn(frozen_label),
            b2_rect.animate.set_stroke(color="#06b6d4", width=3.5),
            run_time=1.0,
        )
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 4: TRAINABLE MODULES HIGHLIGHT (Router & Refiner)
        # ============================================================
        trainable_label = Text("★ Trainable Modules (Lightweight ~ Few Parameters)", font_size=15, color=YELLOW, weight=BOLD)
        trainable_label.to_edge(DOWN, buff=0.5)

        trainable_box = SurroundingRectangle(
            trainable_label, color=YELLOW, buff=0.15, stroke_width=1.5, corner_radius=0.1, fill_color="#2d1f05", fill_opacity=0.65,
        )
        trainable_group = VGroup(trainable_box, trainable_label)

        # Glowing ring circumscribing Router & Refiner + Show Trainable label
        self.play(
            Circumscribe(b1_rect, color=YELLOW, stroke_width=4, time_width=0.6),
            Circumscribe(b3_rect, color=YELLOW, stroke_width=4, time_width=0.6),
            FadeIn(trainable_group, shift=UP * 0.2),
            b1_rect.animate.set_stroke(color=YELLOW, width=3.5),
            b3_rect.animate.set_stroke(color=YELLOW, width=3.5),
            run_time=1.4,
        )
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 5: END-TO-END DATA FLOW ANIMATION
        # ============================================================
        p1 = Dot(radius=0.09, color=YELLOW).move_to(b1_rect.get_left())
        path = Line(b1_rect.get_left(), b3_rect.get_right())

        self.play(
            MoveAlongPath(p1, path, rate_func=linear, run_time=1.8),
            Flash(b1_rect.get_center(), color=GREEN, line_length=0.25, run_time=0.6),
            Flash(b2_rect.get_center(), color=BLUE, line_length=0.25, run_time=0.6),
            Flash(b3_rect.get_center(), color=PURPLE, line_length=0.25, run_time=0.6),
        )
        self.remove(p1)
        self.wait(WAIT_LONG)
