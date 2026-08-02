"""
boxes.py — Box components tái sử dụng: InfoBox, HighlightBox, CodeBlock.

Sử dụng:
    from components.boxes import *

    info = InfoBox("Note", "This is important information")
    highlight = HighlightBox(some_mobject, color=ACCENT)
    code = CodeBlock("x = 42\\nprint(x)")
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from utils.colors import *


class InfoBox(VGroup):
    """
    Hộp thông tin có tiêu đề và nội dung.

    Args:
        title: Tiêu đề box
        content: Nội dung text
        width: Chiều rộng (None = tự tính)
        bg_color: Màu nền
        border_color: Màu viền
        title_color: Màu tiêu đề
        content_color: Màu nội dung
        corner_radius: Bo góc
    """

    def __init__(self, title: str, content: str, width: float = None,
                 bg_color=BG_MEDIUM, border_color=PRIMARY,
                 title_color=PRIMARY_LIGHT, content_color=TEXT_PRIMARY,
                 corner_radius: float = 0.15, **kwargs):
        super().__init__(**kwargs)

        # Title text
        title_mob = Text(
            title, font_size=28, color=title_color, weight=BOLD
        )

        # Content text
        content_mob = Text(
            content, font_size=22, color=content_color, line_spacing=1.3
        )

        # Stack title + content
        text_group = VGroup(title_mob, content_mob).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        # Calculate box size
        box_width = width or (text_group.width + 0.8)
        box_height = text_group.height + 0.7

        # Background rectangle
        bg_rect = RoundedRectangle(
            width=box_width,
            height=box_height,
            corner_radius=corner_radius,
            fill_color=bg_color,
            fill_opacity=0.85,
            stroke_color=border_color,
            stroke_width=2,
        )

        # Title accent bar (thanh màu bên trái)
        accent_bar = Line(
            start=bg_rect.get_corner(UL) + DOWN * 0.15 + RIGHT * 0.12,
            end=bg_rect.get_corner(DL) + UP * 0.15 + RIGHT * 0.12,
            color=border_color,
            stroke_width=4,
        )

        text_group.move_to(bg_rect.get_center())

        self.add(bg_rect, accent_bar, text_group)
        self.bg_rect = bg_rect
        self.title_mob = title_mob
        self.content_mob = content_mob


class HighlightBox(VGroup):
    """
    Hộp highlight bao quanh một mobject có sẵn.

    Args:
        mobject: Object cần bao quanh
        color: Màu viền + glow
        padding: Khoảng đệm xung quanh object
        corner_radius: Bo góc
        fill_opacity: Độ trong suốt nền
    """

    def __init__(self, mobject: Mobject = None, color=PRIMARY,
                 padding: float = 0.3, corner_radius: float = 0.15,
                 fill_opacity: float = 0.1, stroke_width: float = 2.5,
                 **kwargs):
        super().__init__(**kwargs)

        if mobject is not None:
            w = mobject.width + 2 * padding
            h = mobject.height + 2 * padding
        else:
            w = 3.0
            h = 1.5

        self.box = RoundedRectangle(
            width=w,
            height=h,
            corner_radius=corner_radius,
            fill_color=color,
            fill_opacity=fill_opacity,
            stroke_color=color,
            stroke_width=stroke_width,
        )

        if mobject is not None:
            self.box.move_to(mobject.get_center())

        self.add(self.box)

    def surround(self, mobject: Mobject, padding: float = 0.3):
        """Cập nhật vị trí và kích thước bao quanh mobject."""
        self.box.stretch_to_fit_width(mobject.width + 2 * padding)
        self.box.stretch_to_fit_height(mobject.height + 2 * padding)
        self.box.move_to(mobject.get_center())
        return self


class CodeBlock(VGroup):
    """
    Hiển thị code với style giống code editor.

    Args:
        code: String code (dùng \\n cho xuống dòng)
        language_label: Nhãn ngôn ngữ (vd: "Python")
        width: Chiều rộng (None = tự tính)
        font_size: Cỡ chữ code
    """

    def __init__(self, code: str, language_label: str = None,
                 width: float = None, font_size: int = 20,
                 bg_color="#1e1e2e", border_color="#3a3a5a",
                 text_color="#e0e0e0", **kwargs):
        super().__init__(**kwargs)

        # Code text (dùng Monospace)
        code_text = Text(
            code,
            font="Monospace",
            font_size=font_size,
            color=text_color,
            line_spacing=1.4,
        )

        # Background
        box_width = width or (code_text.width + 1.0)
        box_height = code_text.height + 0.8

        bg = RoundedRectangle(
            width=box_width,
            height=box_height,
            corner_radius=0.12,
            fill_color=bg_color,
            fill_opacity=0.95,
            stroke_color=border_color,
            stroke_width=1.5,
        )

        code_text.move_to(bg.get_center())

        # Language label (góc trên phải)
        if language_label:
            label = Text(
                language_label, font_size=14, color=TEXT_MUTED
            )
            label.next_to(bg, UP, buff=0.05).align_to(bg, RIGHT)
            self.add(label)

        # Dot decoration (kiểu macOS window)
        dots = VGroup()
        for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
            dot = Dot(radius=0.06, color=c)
            dots.add(dot)
        dots.arrange(RIGHT, buff=0.12)
        dots.next_to(bg, UP, buff=0.0).align_to(bg, LEFT).shift(RIGHT * 0.25 + DOWN * 0.25)

        self.add(bg, dots, code_text)
        self.bg = bg
        self.code_text = code_text


class GlassPanel(VGroup):
    """
    Panel kiểu glassmorphism (kính mờ).

    Args:
        width: Chiều rộng
        height: Chiều cao
        bg_color: Màu nền
        fill_opacity: Độ trong suốt
        border_color: Màu viền
    """

    def __init__(self, width: float = 5, height: float = 3,
                 bg_color=BG_MEDIUM, fill_opacity: float = 0.4,
                 border_color=None, corner_radius: float = 0.2,
                 **kwargs):
        super().__init__(**kwargs)

        border_c = border_color or ManimColor(TEXT_MUTED)

        self.panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            fill_color=bg_color,
            fill_opacity=fill_opacity,
            stroke_color=border_c,
            stroke_width=1.0,
        )
        self.add(self.panel)

    def add_content(self, mobject: Mobject, buff: float = 0.3):
        """Thêm content vào giữa panel."""
        mobject.move_to(self.panel.get_center())
        self.add(mobject)
        return self
