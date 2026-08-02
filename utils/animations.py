"""
animations.py — Custom animations tái sử dụng.

Sử dụng:
    from utils.animations import *

    # Trong construct():
    self.play(fade_in_shift(title, direction=UP))
    self.play(*sequential_fade_in(items, delay=0.15))
    self.play(highlight_pulse(node))
"""

from manim import *
import numpy as np


def fade_in_shift(mobject: Mobject, direction=UP, shift_distance: float = 0.5,
                  run_time: float = 0.8) -> Animation:
    """
    Fade in kèm dịch chuyển từ một hướng.

    Args:
        mobject: Object cần animate
        direction: Hướng dịch chuyển (UP, DOWN, LEFT, RIGHT)
        shift_distance: Khoảng cách dịch
        run_time: Thời gian animation
    """
    return FadeIn(mobject, shift=direction * shift_distance, run_time=run_time)


def fade_out_shift(mobject: Mobject, direction=DOWN, shift_distance: float = 0.5,
                   run_time: float = 0.6) -> Animation:
    """Fade out kèm dịch chuyển."""
    return FadeOut(mobject, shift=direction * shift_distance, run_time=run_time)


def sequential_fade_in(mobjects: list, direction=UP, shift_distance: float = 0.4,
                        lag_ratio: float = 0.15) -> AnimationGroup:
    """
    Fade in lần lượt một danh sách objects với delay giữa mỗi object.

    Args:
        mobjects: Danh sách Mobjects
        direction: Hướng fade in
        shift_distance: Khoảng dịch
        lag_ratio: Tỷ lệ delay giữa các object (0-1)

    Returns:
        AnimationGroup có thể dùng trong self.play()
    """
    animations = [
        FadeIn(mob, shift=direction * shift_distance)
        for mob in mobjects
    ]
    return AnimationGroup(*animations, lag_ratio=lag_ratio)


def highlight_pulse(mobject: Mobject, color=None, scale_factor: float = 1.15,
                    run_time: float = 0.8) -> Succession:
    """
    Hiệu ứng nhấp nháy highlight — phóng to rồi thu lại.

    Args:
        mobject: Object cần highlight
        color: Màu highlight (None = giữ nguyên)
        scale_factor: Hệ số phóng to
        run_time: Tổng thời gian
    """
    half_time = run_time / 2
    anims = [
        mobject.animate(run_time=half_time).scale(scale_factor),
        mobject.animate(run_time=half_time).scale(1 / scale_factor),
    ]
    if color:
        anims = [
            mobject.animate(run_time=half_time).scale(scale_factor).set_color(color),
            mobject.animate(run_time=half_time).scale(1 / scale_factor),
        ]
    return Succession(*anims)


def sweep_in(mobject: Mobject, direction=LEFT, run_time: float = 0.8) -> Animation:
    """
    Quét object vào từ ngoài màn hình.

    Args:
        mobject: Object cần animate
        direction: Hướng quét VÀO (LEFT = object bay từ phải sang trái vào)
        run_time: Thời gian animation
    """
    offset = direction * 15  # Đẩy ra ngoài màn hình
    return FadeIn(mobject, shift=offset, run_time=run_time)


def typewriter_text(scene, text_mobject: Mobject, time_per_char: float = 0.05,
                    cursor: bool = False):
    """
    Hiệu ứng đánh máy — hiện từng ký tự.

    Lưu ý: Hàm này gọi scene.play() trực tiếp, dùng trong construct().

    Args:
        scene: Scene instance (self)
        text_mobject: Text hoặc Tex mobject
        time_per_char: Thời gian mỗi ký tự
        cursor: Có hiện con trỏ nhấp nháy không
    """
    scene.play(AddTextLetterByLetter(text_mobject, time_per_char=time_per_char))


def scale_fade_in(mobject: Mobject, start_scale: float = 0.5,
                  run_time: float = 0.7) -> AnimationGroup:
    """
    Fade in kèm scale từ nhỏ lên to (kiểu pop-in).

    Args:
        mobject: Object cần animate
        start_scale: Scale ban đầu (< 1 = nhỏ hơn)
        run_time: Thời gian animation
    """
    mobject.scale(start_scale)
    return AnimationGroup(
        FadeIn(mobject, run_time=run_time),
        mobject.animate(run_time=run_time).scale(1 / start_scale),
    )


def transform_color(mobject: Mobject, target_color, run_time: float = 0.5) -> Animation:
    """Chuyển đổi màu mượt mà."""
    return mobject.animate(run_time=run_time).set_color(target_color)


def blink(mobject: Mobject, times: int = 2, run_time: float = 1.0) -> Succession:
    """
    Nhấp nháy object (ẩn/hiện).

    Args:
        mobject: Object cần blink
        times: Số lần nhấp nháy
        run_time: Tổng thời gian
    """
    single = run_time / (times * 2)
    anims = []
    for _ in range(times):
        anims.append(FadeOut(mobject, run_time=single))
        anims.append(FadeIn(mobject, run_time=single))
    return Succession(*anims)


def draw_then_fade(mobject: Mobject, hold_time: float = 1.0,
                   draw_time: float = 1.0, fade_time: float = 0.5) -> Succession:
    """
    Vẽ object (Create), giữ một lúc, rồi fade out.

    Args:
        mobject: VMobject cần animate
        hold_time: Thời gian giữ sau khi vẽ
        draw_time: Thời gian vẽ
        fade_time: Thời gian fade out
    """
    return Succession(
        Create(mobject, run_time=draw_time),
        Wait(hold_time),
        FadeOut(mobject, run_time=fade_time),
    )
