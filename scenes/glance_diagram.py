"""
Sơ đồ kiến trúc GLANCE (Figure 2) dựng bằng Manim Community.

Chạy bằng:
    manim -pql scenes/glance_diagram.py GlanceArchitecture      # xem trước
    manim -pqh scenes/glance_diagram.py GlanceArchitecture      # render HD

Chia làm 3 khối lớn tương ứng 3 bước của GLANCE:
    Step 1: Generate and Process Routing Features (Router)
    Step 2: Use Pre-trained LLM to Process Routed Neighborhoods
    Step 3: Refine the GNN predictions using LLM embeddings (Refiner)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
import numpy as np


class GlanceArchitecture(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(color=BLACK, font="Arial")

        title = Text("GLANCE: Node-Aware GNN-LLM Fusion", font_size=30, color=BLACK)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ================= STEP 1: ROUTING FEATURES =================
        step1_label = Text("Step 1: Routing Features", font_size=20, color=BLUE_E)
        step1_box = SurroundingRectangle(step1_label, buff=0.15, color=BLUE_E)

        # Input graph node (TAG)
        tag_dot = Dot(radius=0.08, color=GRAY)
        tag_label = Text("TAG", font_size=16, color=BLACK).next_to(tag_dot, DOWN, buff=0.15)
        tag_group = VGroup(tag_dot, tag_label)

        # 3 encoder
        gnn_box = RoundedRectangle(width=1.3, height=0.6, corner_radius=0.1, color=ORANGE, fill_color=ORANGE, fill_opacity=0.25)
        gnn_text = Text("GNN", font_size=18, color=BLACK).move_to(gnn_box)
        gnn_group = VGroup(gnn_box, gnn_text)

        mlp_box = RoundedRectangle(width=1.3, height=0.6, corner_radius=0.1, color=GREEN, fill_color=GREEN, fill_opacity=0.25)
        mlp_text = Text("MLP (Q)", font_size=16, color=BLACK).move_to(mlp_box)
        mlp_group = VGroup(mlp_box, mlp_text)

        feat_box = RoundedRectangle(width=1.3, height=0.6, corner_radius=0.1, color=PURPLE, fill_color=PURPLE, fill_opacity=0.25)
        feat_text = Text("Features", font_size=16, color=BLACK).move_to(feat_box)
        feat_group = VGroup(feat_box, feat_text)

        encoders = VGroup(gnn_group, mlp_group, feat_group).arrange(DOWN, buff=0.25)

        # Routing features list
        signal_items = [
            "Node Embedding  z_G(v)",
            "Node Uncertainty",
            "Homophily Est.  h_v",
            "Node Features",
            "Degree  d_v",
        ]
        signal_texts = VGroup(*[
            Text(s, font_size=14, color=BLACK) for s in signal_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        signal_box = SurroundingRectangle(signal_texts, buff=0.15, color=GRAY_B)
        signal_group = VGroup(signal_box, signal_texts)

        # Router: sigma(sum) -> a_v
        router_circle = Circle(radius=0.35, color=RED, fill_color=RED, fill_opacity=0.15)
        router_text = MathTex(r"\sigma\!\left(\sum\right)", font_size=22, color=BLACK).move_to(router_circle)
        router_group = VGroup(router_circle, router_text)

        route_yes = Text("Route Y", font_size=16, color=GREEN_E)
        route_no = Text("Route X", font_size=16, color=RED_E)

        # Layout Step 1
        step1_content = VGroup(tag_group, encoders, signal_group, router_group).arrange(RIGHT, buff=0.7)
        step1_content.scale(0.85)

        step1_all = VGroup(step1_label, step1_content)
        step1_all.arrange(DOWN, buff=0.3)
        step1_outer_box = SurroundingRectangle(step1_all, buff=0.25, color=BLUE_E, corner_radius=0.1)

        step1_full = VGroup(step1_outer_box, step1_all)
        step1_full.scale(0.9).to_edge(LEFT, buff=0.4).shift(UP * 0.3)

        route_yes.next_to(router_group, DOWN, buff=0.3).shift(RIGHT * 0.3)
        route_no.next_to(router_group, DOWN, buff=0.3).shift(LEFT * 0.3)

        arrows_step1 = VGroup(
            Arrow(tag_group.get_right(), encoders.get_left(), buff=0.1, color=BLACK, stroke_width=2),
            Arrow(encoders.get_right(), signal_group.get_left(), buff=0.1, color=BLACK, stroke_width=2),
            Arrow(signal_group.get_right(), router_group.get_left(), buff=0.1, color=BLACK, stroke_width=2),
        )

        self.play(Create(step1_outer_box), Write(step1_label))
        self.play(FadeIn(tag_group))
        self.play(FadeIn(encoders), Create(arrows_step1[0]))
        self.play(FadeIn(signal_group), Create(arrows_step1[1]))
        self.play(FadeIn(router_group), Create(arrows_step1[2]))
        self.play(Write(route_yes), Write(route_no))
        self.wait(0.5)

        # ================= STEP 2: LLM MULTI-HOP ENCODING =================
        step2_label = Text("Step 2: LLM Multi-hop Encoding", font_size=20, color=PURPLE_E)

        hop_rows = []
        hop_names = ["Ego (0-hop)", "1-hop", "2-hop"]
        for name in hop_names:
            hop_text = Text(name, font_size=14, color=BLACK)
            llm_box = RoundedRectangle(width=1.6, height=0.55, corner_radius=0.1,
                                        color=PURPLE, fill_color=PURPLE, fill_opacity=0.25)
            llm_text = Text("LLM (Qwen-8B)", font_size=13, color=BLACK).move_to(llm_box)
            emb_rect = Rectangle(width=0.5, height=0.4, color=BLACK)
            row = VGroup(hop_text, llm_box, llm_text, emb_rect).arrange(RIGHT, buff=0.25)
            llm_text.move_to(llm_box)
            hop_rows.append(row)

        hop_group = VGroup(*hop_rows).arrange(DOWN, buff=0.3)
        step2_all = VGroup(step2_label, hop_group).arrange(DOWN, buff=0.3)
        step2_outer_box = SurroundingRectangle(step2_all, buff=0.25, color=PURPLE_E, corner_radius=0.1)
        step2_full = VGroup(step2_outer_box, step2_all)
        step2_full.scale(0.75).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.play(Create(step2_outer_box), Write(step2_label))
        for row in hop_rows:
            self.play(FadeIn(row), run_time=0.4)

        concat_brace = Brace(hop_group, direction=RIGHT, color=BLACK)
        concat_text = MathTex(
            r"z_L(v)=[z_{L,0}\|z_{L,1}\|z_{L,2}]", font_size=20, color=BLACK
        ).next_to(concat_brace, RIGHT, buff=0.15)
        self.play(GrowFromCenter(concat_brace), Write(concat_text))
        self.wait(0.5)

        # Arrow Route Y -> Step 2
        connector_1_2 = Arrow(
            route_yes.get_top(), step2_outer_box.get_left(),
            buff=0.2, color=GOLD_E, stroke_width=3
        )
        self.play(Create(connector_1_2))
        self.wait(0.3)

        # ================= STEP 3: REFINER =================
        step3_label = Text("Step 3: Refiner (Prediction Fusion)", font_size=20, color=GREEN_E)

        gnn_emb_box = Rectangle(width=1.4, height=0.5, color=ORANGE)
        gnn_emb_text = Text("GNN Emb.", font_size=13, color=BLACK).move_to(gnn_emb_box)
        gnn_emb_group = VGroup(gnn_emb_box, gnn_emb_text)

        llm_emb_box = Rectangle(width=1.4, height=0.5, color=PURPLE)
        llm_emb_text = Text("LLM Emb.", font_size=13, color=BLACK).move_to(llm_emb_box)
        llm_emb_group = VGroup(llm_emb_box, llm_emb_text)

        concat_symbol = MathTex(r"\|", font_size=28, color=BLACK)

        refiner_box = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.1,
                                        color=GREEN, fill_color=GREEN, fill_opacity=0.25)
        refiner_text = Text("Refiner\nMLP C", font_size=14, color=BLACK).move_to(refiner_box)
        refiner_group = VGroup(refiner_box, refiner_text)

        pred_box = Rectangle(width=1.4, height=0.5, color=BLACK)
        pred_text = MathTex(r"p_{C,v}", font_size=18, color=BLACK).move_to(pred_box)
        pred_group = VGroup(pred_box, pred_text)

        fusion_row = VGroup(
            gnn_emb_group, concat_symbol, llm_emb_group
        ).arrange(RIGHT, buff=0.2)

        refiner_row = VGroup(refiner_group, pred_group).arrange(RIGHT, buff=0.4)
        step3_stack = VGroup(fusion_row, refiner_row).arrange(DOWN, buff=0.4)
        step3_all = VGroup(step3_label, step3_stack).arrange(DOWN, buff=0.3)
        step3_outer_box = SurroundingRectangle(step3_all, buff=0.25, color=GREEN_E, corner_radius=0.1)
        step3_full = VGroup(step3_outer_box, step3_all)
        step3_full.scale(0.75).next_to(step1_full, DOWN, buff=0.6).align_to(step1_full, LEFT)

        arrow_fuse_to_refiner = Arrow(
            fusion_row.get_bottom(), refiner_group.get_top(), buff=0.1, color=BLACK, stroke_width=2
        )
        arrow_refiner_to_pred = Arrow(
            refiner_group.get_right(), pred_group.get_left(), buff=0.1, color=BLACK, stroke_width=2
        )

        self.play(
            Create(step3_outer_box), Write(step3_label),
            FadeIn(gnn_emb_group), FadeIn(concat_symbol), FadeIn(llm_emb_group),
        )
        self.play(Create(arrow_fuse_to_refiner), FadeIn(refiner_group))
        self.play(Create(arrow_refiner_to_pred), FadeIn(pred_group))
        self.wait(0.3)

        # Connectors
        connector_2_3 = Arrow(
            step2_full.get_bottom(), llm_emb_group.get_top(),
            buff=0.2, color=GOLD_E, stroke_width=3
        )
        connector_1_pred = Arrow(
            route_no.get_bottom(), gnn_emb_group.get_top(),
            buff=0.2, color=GRAY, stroke_width=2
        )
        self.play(Create(connector_2_3), Create(connector_1_pred))

        final_note = Text(
            "Only Router and Refiner are trained -- GNN & LLM are frozen",
            font_size=16, color=BLACK
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(final_note))

        self.wait(2)
