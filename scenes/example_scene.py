"""
example_scene.py — Scene mẫu minh họa cách sử dụng components và utils.

Render:
    manim -pql scenes/example_scene.py ExampleScene
"""

import sys
import os

# Thêm project root vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from config import *
from utils import *
from components import *


class ExampleScene(Scene):
    """Scene mẫu demo toàn bộ components và utils."""

    def construct(self):
        # ----- Áp dụng cấu hình toàn cục -----
        apply_scene_config(self)

        # =====================================================================
        # PHẦN 1: Title Screen
        # =====================================================================
        title = StyledTitle("Manim Boilerplate")
        subtitle = StyledSubtitle("Demo — Components & Utils")
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.4)

        self.play(fade_in_shift(title, direction=DOWN))
        self.play(fade_in_shift(subtitle, direction=UP))
        self.wait(WAIT_LONG)
        self.play(FadeOut(title_group))

        # =====================================================================
        # PHẦN 2: Text Styles
        # =====================================================================
        section = SectionTitle("Text Styles", "Các kiểu text có sẵn")
        section.to_edge(UP, buff=0.5)
        self.play(fade_in_shift(section))

        bullets = BulletList([
            "StyledTitle — Tiêu đề lớn",
            "StyledBody — Nội dung chính",
            "StyledCaption — Chú thích nhỏ",
        ])
        bullets.next_to(section, DOWN, buff=0.6)
        self.play(sequential_fade_in(bullets.submobjects))
        self.wait(WAIT_LONG)
        self.play(FadeOut(section), FadeOut(bullets))

        # =====================================================================
        # PHẦN 3: Boxes
        # =====================================================================
        info = InfoBox("Tip", "InfoBox component\nwith accent bar")
        code = CodeBlock("x = 42\nprint(x)", language_label="Python")
        box_group = arrange_row([info, code], buff=1.0)

        self.play(sequential_fade_in([info, code], lag_ratio=0.3))
        self.wait(WAIT_LONG)

        # Highlight box demo
        highlight = HighlightBox(code, color=ACCENT)
        self.play(Create(highlight.box))
        self.wait(WAIT_MEDIUM)
        self.play(FadeOut(box_group), FadeOut(highlight))

        # =====================================================================
        # PHẦN 4: Arrows & Annotations
        # =====================================================================
        circle_a = Circle(radius=0.5, color=PRIMARY, fill_opacity=0.3)
        circle_b = Circle(radius=0.5, color=SECONDARY, fill_opacity=0.3)
        label_a = Text("A", font_size=28, color=TEXT_PRIMARY).move_to(circle_a)
        label_b = Text("B", font_size=28, color=TEXT_PRIMARY).move_to(circle_b)
        node_a = VGroup(circle_a, label_a).shift(LEFT * 3)
        node_b = VGroup(circle_b, label_b).shift(RIGHT * 3)

        arrow = LabeledArrow(
            "connection",
            start=node_a.get_right(),
            end=node_b.get_left(),
            color=ACCENT,
        )

        callout = Callout("This is node A", node_a, direction=UP, color=WARNING)

        self.play(FadeIn(node_a), FadeIn(node_b))
        self.play(Create(arrow.arrow), FadeIn(arrow.label))
        self.play(FadeIn(callout))
        self.wait(WAIT_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # =====================================================================
        # PHẦN 5: Color Palette Demo
        # =====================================================================
        palette_title = StyledHeading("Color Palette")
        palette_title.to_edge(UP, buff=0.5)
        self.play(fade_in_shift(palette_title))

        color_squares = []
        colors_demo = [PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, ERROR, INFO]
        names_demo = ["Primary", "Secondary", "Accent", "Success", "Warning", "Error", "Info"]

        for c, name in zip(colors_demo, names_demo):
            sq = Square(side_length=0.8, fill_color=c, fill_opacity=0.9,
                       stroke_width=0)
            label = Text(name, font_size=14, color=TEXT_PRIMARY)
            label.next_to(sq, DOWN, buff=0.15)
            color_squares.append(VGroup(sq, label))

        palette = arrange_row(color_squares, buff=0.4)
        palette.next_to(palette_title, DOWN, buff=0.8)

        self.play(sequential_fade_in(color_squares, lag_ratio=0.1))
        self.wait(WAIT_LONG)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # =====================================================================
        # PHẦN 6: Outro
        # =====================================================================
        outro = StyledTitle("Ready to Create!", color=PRIMARY_LIGHT)
        caption = StyledCaption("Add your scenes to scenes/ folder")
        outro_group = VGroup(outro, caption).arrange(DOWN, buff=0.4)

        self.play(scale_fade_in(outro_group, start_scale=0.7))
        self.wait(WAIT_LONG)
        self.play(FadeOut(outro_group))
