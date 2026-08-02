"""
Scene 1: Homophily vs Heterophily
- Tại sao GNN mạnh/yếu theo cấu trúc đồ thị
- Local Homophily formula
- Message passing animation trên 2 đồ thị

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
            font_size=FONT_SIZE_HEADING,
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
            font_size=36,
        )
        formula.next_to(title, DOWN, buff=0.4)

        # --- Hiện title ---
        self.play(fade_in_shift(title, direction=DOWN))
        self.wait(WAIT_SHORT)

        # --- Viết công thức ---
        self.play(Write(formula), run_time=2.0)
        self.wait(WAIT_LONG)

        # --- Thu nhỏ vào góc trên trái ---
        title_formula = VGroup(title, formula)
        self.play(
            title_formula.animate.scale(0.45).to_corner(UL, buff=0.25),
            run_time=ANIM_SPEED_NORMAL,
        )
        self.wait(WAIT_SHORT)

        # ============================================================
        # PHASE 2: VẼ 2 ĐỒ THỊ (Trái & Phải)
        # ============================================================

        # --- Cấu hình chung ---
        CENTER_R = 0.38          # Bán kính node trung tâm
        NEIGHBOR_R = 0.28        # Bán kính node hàng xóm
        ORBIT = 1.5              # Khoảng cách neighbor → center
        GRAPH_Y = -0.2           # Vị trí y của graph

        # ==========================
        # ĐỒ THỊ TRÁI: HOMOPHILY
        # ==========================
        left_pos = np.array([-3.3, GRAPH_Y, 0])

        # Center node (GREEN)
        l_center = Circle(
            radius=CENTER_R, color=GREEN,
            fill_opacity=0.85, stroke_width=2.5,
        ).move_to(left_pos)
        l_center_v = Text("v", font_size=18, color=WHITE, weight=BOLD)
        l_center_v.move_to(left_pos)

        # 4 neighbors (tất cả GREEN) — 4 góc: 45°, 135°, 225°, 315°
        l_angles = [PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4]
        l_neighbors = []
        l_edges = []

        for angle in l_angles:
            pos = left_pos + np.array([
                np.cos(angle), np.sin(angle), 0
            ]) * ORBIT

            node = Circle(
                radius=NEIGHBOR_R, color=GREEN,
                fill_opacity=0.55, stroke_width=2,
            ).move_to(pos)
            l_neighbors.append(node)

            edge = Line(
                left_pos, pos,
                color=EDGE_COLOR, stroke_width=2.5,
            )
            l_edges.append(edge)

        # Label
        l_label = Text(
            "Homophily: GNN Strong",
            font_size=22, color=GREEN, weight=BOLD,
        )
        l_all_nodes = VGroup(l_center, *l_neighbors)
        l_label.next_to(l_all_nodes, DOWN, buff=0.5)

        # ==========================
        # ĐỒ THỊ PHẢI: HETEROPHILY
        # ==========================
        right_pos = np.array([3.3, GRAPH_Y, 0])

        # Center node (GREEN)
        r_center = Circle(
            radius=CENTER_R, color=GREEN,
            fill_opacity=0.85, stroke_width=2.5,
        ).move_to(right_pos)
        r_center_v = Text("v", font_size=18, color=WHITE, weight=BOLD)
        r_center_v.move_to(right_pos)

        # 3 neighbors: RED, YELLOW, PURPLE — 3 góc: 90°, 210°, 330°
        r_colors = [RED, YELLOW, PURPLE]
        r_angles = [PI / 2, 7 * PI / 6, 11 * PI / 6]
        r_neighbors = []
        r_edges = []

        for angle, nc in zip(r_angles, r_colors):
            pos = right_pos + np.array([
                np.cos(angle), np.sin(angle), 0
            ]) * ORBIT

            node = Circle(
                radius=NEIGHBOR_R, color=nc,
                fill_opacity=0.55, stroke_width=2,
            ).move_to(pos)
            r_neighbors.append(node)

            edge = Line(
                right_pos, pos,
                color=EDGE_COLOR, stroke_width=2.5,
            )
            r_edges.append(edge)

        # Label
        r_label = Text(
            "Heterophily: GNN Weak",
            font_size=22, color=RED, weight=BOLD,
        )
        r_all_nodes = VGroup(r_center, *r_neighbors)
        r_label.next_to(r_all_nodes, DOWN, buff=0.5)

        # --- Đường phân cách giữa 2 đồ thị ---
        divider = DashedLine(
            UP * 3, DOWN * 3.5,
            color=TEXT_MUTED, stroke_width=1, dash_length=0.15,
        )

        # ==========================
        # ANIMATE: Vẽ đồ thị
        # ==========================

        # Đường phân cách
        self.play(Create(divider), run_time=0.4)

        # Edges (cả 2 đồ thị cùng lúc)
        self.play(
            *[Create(e) for e in l_edges + r_edges],
            run_time=ANIM_SPEED_NORMAL,
        )

        # Nodes (cả 2 đồ thị cùng lúc)
        all_nodes = (
            [l_center] + l_neighbors + [r_center] + r_neighbors
        )
        self.play(
            *[GrowFromCenter(n) for n in all_nodes],
            run_time=ANIM_SPEED_NORMAL,
        )

        # Labels "v" trên center nodes
        self.play(
            FadeIn(l_center_v, scale=0.5),
            FadeIn(r_center_v, scale=0.5),
            run_time=0.4,
        )

        # Labels dưới đồ thị
        self.play(
            fade_in_shift(l_label, direction=UP, shift_distance=0.3),
            fade_in_shift(r_label, direction=UP, shift_distance=0.3),
        )
        self.wait(WAIT_LONG)

        # ============================================================
        # PHASE 3: MESSAGE PASSING ANIMATION
        # ============================================================

        DOT_R = 0.1

        # --- Tạo dots tại vị trí neighbor ---
        l_dots = []
        for nb in l_neighbors:
            dot = Dot(radius=DOT_R, color=GREEN, fill_opacity=1)
            dot.move_to(nb.get_center())
            l_dots.append(dot)

        r_dots = []
        for nb, nc in zip(r_neighbors, r_colors):
            dot = Dot(radius=DOT_R, color=nc, fill_opacity=1)
            dot.move_to(nb.get_center())
            r_dots.append(dot)

        # --- Hiện dots ---
        self.play(
            *[FadeIn(d, scale=0.3) for d in l_dots + r_dots],
            run_time=0.5,
        )
        self.wait(WAIT_SHORT)

        # --- Di chuyển dots dọc theo edges vào center (cả 2 đồ thị cùng lúc) ---
        move_anims = []
        for dot in l_dots:
            path = Line(dot.get_center(), l_center.get_center())
            move_anims.append(MoveAlongPath(dot, path))

        for dot in r_dots:
            path = Line(dot.get_center(), r_center.get_center())
            move_anims.append(MoveAlongPath(dot, path))

        self.play(*move_anims, run_time=1.8, rate_func=smooth)

        # --- Xóa dots ---
        self.remove(*l_dots, *r_dots)

        # --- Hiệu ứng tại center nodes ---
        # Trái: Sáng lên (thành công!) — Circumscribe
        # Phải: Rung lắc (lỗi!)     — Wiggle
        self.play(
            Circumscribe(
                l_center, color=GREEN,
                fade_out=True, run_time=1.5,
            ),
            Wiggle(
                r_center, scale_value=1.3,
                rotation_angle=0.06 * TAU, run_time=1.5,
            ),
        )
        self.wait(WAIT_MEDIUM)

        # ============================================================
        # PHASE 4: HIỆN h_v → 1 / h_v → 0
        # ============================================================
        hv_left = MathTex(r"h_v \to 1", font_size=28, color=GREEN)
        hv_left.next_to(l_label, DOWN, buff=0.3)

        hv_right = MathTex(r"h_v \to 0", font_size=28, color=RED)
        hv_right.next_to(r_label, DOWN, buff=0.3)

        self.play(
            FadeIn(hv_left, shift=UP * 0.2),
            FadeIn(hv_right, shift=UP * 0.2),
        )
        self.wait(WAIT_EXTRA_LONG)
