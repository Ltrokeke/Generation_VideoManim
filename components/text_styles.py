"""
text_styles.py — Styled text components tái sử dụng.

Sử dụng:
    from components.text_styles import *

    title = StyledTitle("Graph Neural Networks")
    subtitle = StyledSubtitle("An Introduction")
    caption = StyledCaption("Figure 1: Architecture overview")
    bullets = BulletList(["Point 1", "Point 2", "Point 3"])
"""

import sys
import os

# Thêm project root vào sys.path để import từ thư mục gốc
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from utils.colors import *


# =============================================================================
# FONT CONFIG (import-safe defaults, sẽ bị override nếu config.py được import)
# =============================================================================
_FONT = "sans-serif"
_TITLE_SIZE = 56
_SUBTITLE_SIZE = 40
_HEADING_SIZE = 36
_BODY_SIZE = 30
_CAPTION_SIZE = 24
_SMALL_SIZE = 20


# =============================================================================
# STYLED TEXT COMPONENTS
# =============================================================================

class StyledTitle(Text):
    """Tiêu đề lớn, đậm, màu trắng."""

    def __init__(self, text: str, color=TEXT_PRIMARY, **kwargs):
        super().__init__(
            text,
            font=_FONT,
            font_size=_TITLE_SIZE,
            color=color,
            weight=BOLD,
            **kwargs,
        )


class StyledSubtitle(Text):
    """Phụ đề, nhỏ hơn title, màu phụ."""

    def __init__(self, text: str, color=TEXT_SECONDARY, **kwargs):
        super().__init__(
            text,
            font=_FONT,
            font_size=_SUBTITLE_SIZE,
            color=color,
            **kwargs,
        )


class StyledHeading(Text):
    """Heading cho section, đậm."""

    def __init__(self, text: str, color=PRIMARY_LIGHT, **kwargs):
        super().__init__(
            text,
            font=_FONT,
            font_size=_HEADING_SIZE,
            color=color,
            weight=BOLD,
            **kwargs,
        )


class StyledBody(Text):
    """Text nội dung chính."""

    def __init__(self, text: str, color=TEXT_PRIMARY, **kwargs):
        super().__init__(
            text,
            font=_FONT,
            font_size=_BODY_SIZE,
            color=color,
            **kwargs,
        )


class StyledCaption(Text):
    """Chú thích nhỏ, màu mờ."""

    def __init__(self, text: str, color=TEXT_MUTED, **kwargs):
        super().__init__(
            text,
            font=_FONT,
            font_size=_CAPTION_SIZE,
            color=color,
            slant=ITALIC,
            **kwargs,
        )


class BulletList(VGroup):
    """
    Danh sách bullet points.

    Sử dụng:
        bullets = BulletList([
            "First point here",
            "Second point here",
            "Third point here",
        ])
    """

    def __init__(self, items: list, color=TEXT_PRIMARY, bullet_color=PRIMARY,
                 font_size=None, buff: float = 0.4, indent: float = 0.5,
                 **kwargs):
        super().__init__(**kwargs)
        fs = font_size or _BODY_SIZE

        for item_text in items:
            bullet = Text("•", font_size=fs, color=bullet_color)
            text = Text(item_text, font=_FONT, font_size=fs, color=color)
            row = VGroup(bullet, text).arrange(RIGHT, buff=indent * 0.5)
            self.add(row)

        self.arrange(DOWN, buff=buff, aligned_edge=LEFT)


class SectionTitle(VGroup):
    """
    Tiêu đề section với đường gạch dưới trang trí.

    Sử dụng:
        section = SectionTitle("Architecture", "Overview of GNN layers")
    """

    def __init__(self, title: str, subtitle: str = None,
                 title_color=TEXT_PRIMARY, line_color=PRIMARY, **kwargs):
        super().__init__(**kwargs)

        title_text = StyledHeading(title, color=title_color)
        self.add(title_text)

        # Đường gạch dưới gradient
        underline = Line(
            start=title_text.get_left() + DOWN * 0.2,
            end=title_text.get_right() + DOWN * 0.2,
            color=line_color,
            stroke_width=3,
        )
        self.add(underline)

        if subtitle:
            sub = StyledCaption(subtitle)
            sub.next_to(underline, DOWN, buff=0.2)
            self.add(sub)

        self.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
