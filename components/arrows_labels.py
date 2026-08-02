"""
arrows_labels.py — Annotations: mũi tên có nhãn, ngoặc, callout.

Sử dụng:
    from components.arrows_labels import *

    arrow = LabeledArrow("input", start=LEFT*2, end=RIGHT*2)
    brace = BraceLabel(some_group, "Hidden Layer", direction=DOWN)
    callout = Callout("Important!", target_mob, direction=UP)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from utils.colors import *


class LabeledArrow(VGroup):
    """
    Mũi tên có nhãn text.

    Args:
        label: Text hiển thị trên mũi tên
        start: Điểm bắt đầu
        end: Điểm kết thúc
        color: Màu mũi tên
        label_color: Màu text
        font_size: Cỡ chữ
        label_position: Vị trí text so với mũi tên (UP, DOWN)
        curved: Mũi tên cong hay thẳng
    """

    def __init__(self, label: str, start=LEFT * 2, end=RIGHT * 2,
                 color=TEXT_SECONDARY, label_color=TEXT_PRIMARY,
                 font_size: int = 22, label_position=UP,
                 label_buff: float = 0.15, curved: bool = False,
                 stroke_width: float = 2.5, **kwargs):
        super().__init__(**kwargs)

        # Arrow
        if curved:
            self.arrow = CurvedArrow(
                start, end, color=color, stroke_width=stroke_width
            )
        else:
            self.arrow = Arrow(
                start, end, color=color,
                stroke_width=stroke_width, buff=0,
                max_tip_length_to_length_ratio=0.15,
            )

        # Label
        self.label = Text(label, font_size=font_size, color=label_color)
        self.label.next_to(self.arrow, label_position, buff=label_buff)

        self.add(self.arrow, self.label)


class BraceAnnotation(VGroup):
    """
    Ngoặc nhọn (brace) với text annotation.

    Args:
        mobject: Object cần đánh dấu brace
        text: Text mô tả
        direction: Hướng brace (DOWN, UP, LEFT, RIGHT)
        color: Màu brace
        text_color: Màu text
        font_size: Cỡ chữ
    """

    def __init__(self, mobject: Mobject, text: str, direction=DOWN,
                 color=TEXT_SECONDARY, text_color=TEXT_PRIMARY,
                 font_size: int = 24, **kwargs):
        super().__init__(**kwargs)

        self.brace = Brace(mobject, direction, color=color)
        self.text = Text(text, font_size=font_size, color=text_color)
        self.brace.put_at_tip(self.text)

        self.add(self.brace, self.text)

    def update_target(self, mobject: Mobject):
        """Cập nhật brace cho mobject mới."""
        new_brace = Brace(mobject, self.brace.direction)
        self.brace.become(new_brace)
        self.brace.put_at_tip(self.text)
        return self


class Callout(VGroup):
    """
    Annotation box trỏ đến một object — giống tooltip/speech bubble.

    Args:
        text: Nội dung callout
        target: Mobject mà callout trỏ đến
        direction: Hướng đặt callout so với target (UP, DOWN, LEFT, RIGHT)
        color: Màu viền + mũi tên
        bg_color: Màu nền
        font_size: Cỡ chữ
        width: Chiều rộng cố định (None = tự tính)
    """

    def __init__(self, text: str, target: Mobject = None, direction=UP,
                 color=PRIMARY, bg_color=BG_MEDIUM, font_size: int = 20,
                 width: float = None, buff: float = 0.5, **kwargs):
        super().__init__(**kwargs)

        # Text
        self.text_mob = Text(
            text, font_size=font_size, color=TEXT_PRIMARY, line_spacing=1.2
        )

        # Background box
        box_w = width or (self.text_mob.width + 0.6)
        box_h = self.text_mob.height + 0.4

        self.box = RoundedRectangle(
            width=box_w, height=box_h,
            corner_radius=0.1,
            fill_color=bg_color, fill_opacity=0.9,
            stroke_color=color, stroke_width=2,
        )
        self.text_mob.move_to(self.box.get_center())

        self.add(self.box, self.text_mob)

        # Position relative to target
        if target is not None:
            self.point_to(target, direction, buff)

    def point_to(self, target: Mobject, direction=UP, buff: float = 0.5):
        """
        Đặt callout và thêm mũi tên trỏ đến target.

        Args:
            target: Object đích
            direction: Hướng đặt callout so với target
            buff: Khoảng cách đến target
        """
        # Di chuyển callout
        callout_group = VGroup(self.box, self.text_mob)
        callout_group.next_to(target, direction, buff=buff)

        # Mũi tên từ callout đến target
        if hasattr(self, 'pointer'):
            self.remove(self.pointer)

        # Tính điểm bắt đầu mũi tên (cạnh gần target nhất của box)
        arrow_start = self.box.get_edge_center(-direction)
        arrow_end = target.get_edge_center(direction)

        self.pointer = Arrow(
            arrow_start, arrow_end,
            color=self.box.get_stroke_color(),
            stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )
        self.add(self.pointer)
        return self


class DashedConnection(VGroup):
    """
    Đường nét đứt nối giữa 2 mobjects — dùng để thể hiện quan hệ.

    Args:
        mob_a: Mobject đầu
        mob_b: Mobject cuối
        color: Màu đường
        dash_length: Độ dài mỗi nét đứt
    """

    def __init__(self, mob_a: Mobject, mob_b: Mobject,
                 color=EDGE_COLOR, dash_length: float = 0.15,
                 stroke_width: float = 2, **kwargs):
        super().__init__(**kwargs)

        self.line = DashedLine(
            mob_a.get_center(), mob_b.get_center(),
            color=color, dash_length=dash_length,
            stroke_width=stroke_width,
        )
        self.add(self.line)
