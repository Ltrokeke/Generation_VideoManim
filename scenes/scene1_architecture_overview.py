"""
scene1_architecture_overview.py — GLANCE Architecture Overview (Sequential Reveal Flowchart).

Strict coordinates:
  - Router:       LEFT * 4
  - LLM Encoder:  RIGHT * 3 + UP * 2 (with 'Frozen' badge above)
  - Refiner MLP:  RIGHT * 3 + DOWN * 0.5
  - Final Output: DOWN * 3 (centered along X)

Pure English text, bright white title and crisp colors.
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
        # 1. Áp dụng cấu hình chuẩn của nhóm
        apply_scene_config(self)

        # 2. Tiêu đề màu trắng sáng nổi bật ở đỉnh màn hình
        title = Text(
            "GLANCE Architecture Overview",
            font_size=32,
            weight=BOLD,
            color=WHITE,
        )
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)
        self.wait(WAIT_SHORT)

        # ============================================================
        # ĐỊNH NGHĨA CÁC KHỐI HỘP THEO TỌA ĐỘ
        # ============================================================

        # --- HỘP 1: ROUTER (LEFT * 4) ---
        r1_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.9,
            color=YELLOW, fill_color="#2d2305", fill_opacity=0.88, stroke_width=2.5,
        )
        r1_badge = Text("STEP 1", font_size=11, color=YELLOW, weight=BOLD)
        r1_title = Text("Router", font_size=22, color=WHITE, weight=BOLD)
        r1_sub = Text("Node-level Routing", font_size=12, color=TEXT_SECONDARY)
        r1_content = VGroup(r1_badge, r1_title, r1_sub).arrange(DOWN, buff=0.1)
        router = VGroup(r1_box, r1_content).move_to(LEFT * 4.0)

        # --- HỘP 2: LLM ENCODER (RIGHT * 3 + UP * 2) ---
        llm_box = RoundedRectangle(
            corner_radius=0.15, width=3.4, height=1.6,
            color=BLUE, fill_color="#0d213a", fill_opacity=0.88, stroke_width=2.5,
        )
        llm_badge = Text("STEP 2", font_size=11, color=BLUE_B, weight=BOLD)
        llm_title = Text("LLM Encoder", font_size=20, color=WHITE, weight=BOLD)
        llm_sub = Text("Multi-layer Embedding", font_size=12, color=TEXT_SECONDARY)
        llm_content = VGroup(llm_badge, llm_title, llm_sub).arrange(DOWN, buff=0.1)

        frozen_box = RoundedRectangle(
            corner_radius=0.08, width=1.5, height=0.38,
            color="#06b6d4", fill_color="#083344", fill_opacity=0.95, stroke_width=1.5,
        )
        frozen_txt = Text("Frozen", font_size=11, color="#22d3ee", weight=BOLD)
        frozen_txt.move_to(frozen_box.get_center())
        frozen_badge = VGroup(frozen_box, frozen_txt).next_to(llm_box, UP, buff=0.1)

        llm_group = VGroup(llm_box, llm_content, frozen_badge).move_to(RIGHT * 3.0 + UP * 2.0)

        # --- HỘP 3: REFINER MLP (RIGHT * 3 + DOWN * 0.5) ---
        ref_box = RoundedRectangle(
            corner_radius=0.15, width=3.4, height=1.6,
            color=PURPLE, fill_color="#241238", fill_opacity=0.88, stroke_width=2.5,
        )
        ref_badge = Text("STEP 3", font_size=11, color=PURPLE_B, weight=BOLD)
        ref_title = Text("Refiner MLP", font_size=20, color=WHITE, weight=BOLD)
        ref_sub = Text("Prediction Fusion", font_size=12, color=TEXT_SECONDARY)
        ref_content = VGroup(ref_badge, ref_title, ref_sub).arrange(DOWN, buff=0.1)
        refiner_group = VGroup(ref_box, ref_content).move_to(RIGHT * 3.0 + DOWN * 0.5)

        # --- HỘP 4: FINAL OUTPUT (DOWN * 3, CĂN GIỮA TRỤC X) ---
        out_box = RoundedRectangle(
            corner_radius=0.12, width=6.8, height=0.85,
            color=GRAY, fill_color="#1e293b", fill_opacity=0.9, stroke_width=2.0,
        )
        out_txt = Text("Final Output (GNN Predictions)", font_size=16, color=WHITE, weight=BOLD)
        final_output = VGroup(out_box, out_txt).move_to(DOWN * 3.0)

        # ============================================================
        # BƯỚC 1 (KHỞI TẠO): VẼ ROUTER HIỆN RA ĐẦU TIÊN
        # ============================================================
        self.play(
            Create(r1_box),
            FadeIn(r1_content, shift=UP * 0.2),
            run_time=0.9,
        )
        self.wait(1.0)

        # ============================================================
        # BƯỚC 2 (ROUTE x - EASY NODE BỎ QUA LLM VÀ REFINER)
        # ============================================================
        easy_tag = Text("Easy Node", font_size=15, color=RED, weight=BOLD)
        easy_tag.next_to(router, UP, buff=0.2)

        # Nhấp nháy chữ 'Easy Node'
        self.play(FadeIn(easy_tag, shift=DOWN * 0.1), run_time=0.4)
        self.play(Indicate(easy_tag, color=RED, scale_factor=1.15), run_time=0.5)

        # Hộp Final Output xuất hiện ở đáy
        self.play(FadeIn(final_output, shift=UP * 0.3), run_time=0.7)

        # Mũi tên ĐỎ từ đáy Router -> đỉnh Final Output (nửa bên trái)
        arrow_red_start = r1_box.get_bottom() + LEFT * 0.3
        arrow_red_end = out_box.get_top() + LEFT * 2.0
        arrow_red = Arrow(
            arrow_red_start, arrow_red_end,
            buff=0.1, color=RED, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_red_label = MathTex(r"\text{Route}\;\times", font_size=20, color=RED)
        arrow_red_label.next_to(arrow_red.point_from_proportion(0.5), LEFT, buff=0.15)

        self.play(GrowArrow(arrow_red), FadeIn(arrow_red_label), run_time=0.6)

        # Chấm tròn trắng trượt theo mũi tên Đỏ
        dot_easy = Dot(radius=0.1, color=WHITE).move_to(arrow_red_start)
        self.play(FadeIn(dot_easy, scale=0.5), run_time=0.3)
        self.play(
            MoveAlongPath(dot_easy, Line(arrow_red_start, arrow_red_end), rate_func=smooth),
            run_time=1.0,
        )
        self.play(
            Flash(arrow_red_end, color=RED, line_length=0.2, num_lines=8, run_time=0.5),
        )
        self.remove(dot_easy)
        self.play(FadeOut(easy_tag), run_time=0.3)
        self.wait(1.0)

        # ============================================================
        # BƯỚC 3 (ROUTE v - HARD NODE ĐI QUA LLM VÀ REFINER)
        # ============================================================
        hard_tag = Text("Hard Node", font_size=15, color=GREEN, weight=BOLD)
        hard_tag.next_to(router, UP, buff=0.2)

        # Nhấp nháy chữ 'Hard Node'
        self.play(FadeIn(hard_tag, shift=DOWN * 0.1), run_time=0.4)
        self.play(Indicate(hard_tag, color=GREEN, scale_factor=1.15), run_time=0.5)

        # --- A. Mũi tên XANH LÁ từ Router -> LLM Encoder ---
        arrow_green_start = r1_box.get_right() + UP * 0.2
        arrow_green_end = llm_box.get_left() + DOWN * 0.1
        arrow_green = Arrow(
            arrow_green_start, arrow_green_end,
            buff=0.1, color=GREEN, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.12,
        )
        arrow_green_label = MathTex(r"\text{Route}\;\checkmark", font_size=20, color=GREEN)
        arrow_green_label.next_to(arrow_green.point_from_proportion(0.4), UP, buff=0.12)

        # Vẽ mũi tên xanh lá
        self.play(GrowArrow(arrow_green), FadeIn(arrow_green_label), run_time=0.6)

        # Ngay khi chạm đích -> Create Hộp LLM Encoder hiện ra
        self.play(
            Create(llm_box),
            FadeIn(llm_content, shift=UP * 0.2),
            FadeIn(frozen_badge, shift=DOWN * 0.2),
            run_time=0.8,
        )

        # Chấm tròn trắng trượt từ Router lên LLM
        dot_hard = Dot(radius=0.1, color=WHITE).move_to(arrow_green_start)
        self.play(FadeIn(dot_hard, scale=0.5), run_time=0.3)
        self.play(
            MoveAlongPath(dot_hard, Line(arrow_green_start, arrow_green_end), rate_func=smooth),
            run_time=1.0,
        )
        # LLM phản ứng phát sáng
        self.play(
            Indicate(llm_box, color=BLUE, scale_factor=1.05),
            Wiggle(llm_box, scale_value=1.02, rotation_angle=0.015 * TAU, n_wiggles=3, run_time=0.7),
        )

        # --- B. Mũi tên VÀNG từ LLM Encoder -> Refiner MLP ---
        arrow_yellow_start = llm_box.get_bottom()
        arrow_yellow_end = ref_box.get_top()
        arrow_yellow = Arrow(
            arrow_yellow_start, arrow_yellow_end,
            buff=0.1, color=YELLOW, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_yellow_label = Text("Embed", font_size=12, color=YELLOW, weight=BOLD)
        arrow_yellow_label.next_to(arrow_yellow, RIGHT, buff=0.1)

        self.play(GrowArrow(arrow_yellow), FadeIn(arrow_yellow_label), run_time=0.5)

        # Ngay khi mũi tên vàng chạm đích -> Create Refiner MLP hiện ra
        self.play(
            Create(ref_box),
            FadeIn(ref_content, shift=UP * 0.2),
            run_time=0.8,
        )

        # Chấm tròn trượt xuống Refiner
        self.play(
            MoveAlongPath(dot_hard, Line(arrow_yellow_start, arrow_yellow_end), rate_func=smooth),
            run_time=0.7,
        )
        self.play(Indicate(ref_box, color=PURPLE, scale_factor=1.04), run_time=0.4)

        # --- C. Mũi tên TÍM từ Refiner MLP -> Final Output ---
        arrow_purple_start = ref_box.get_bottom()
        arrow_purple_end = out_box.get_top() + RIGHT * 1.5
        arrow_purple = Arrow(
            arrow_purple_start, arrow_purple_end,
            buff=0.1, color=PURPLE, stroke_width=3.5,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_purple_label = Text("Fuse", font_size=12, color=PURPLE_B, weight=BOLD)
        arrow_purple_label.next_to(arrow_purple, RIGHT, buff=0.1)

        self.play(GrowArrow(arrow_purple), FadeIn(arrow_purple_label), run_time=0.5)

        # Chấm tròn trượt xuống Final Output
        self.play(
            MoveAlongPath(dot_hard, Line(arrow_purple_start, arrow_purple_end), rate_func=smooth),
            run_time=0.7,
        )
        self.play(
            Flash(arrow_purple_end, color=PURPLE, line_length=0.25, num_lines=10, run_time=0.7),
            Circumscribe(final_output, color=WHITE, stroke_width=2.5, time_width=0.5),
        )
        self.remove(dot_hard)
        self.play(FadeOut(hard_tag), run_time=0.3)
        self.wait(WAIT_LONG)
