"""
layout.py — Layout helpers: sắp xếp, căn chỉnh, khoảng cách, và lưu video.

Sử dụng:
    from utils.layout import *

    # Trong construct():
    items = [Circle(), Square(), Triangle()]
    group = arrange_in_grid(items, rows=2, cols=2, buff=0.5)
    self.add(group)

    title = Text("Hello")
    pin_to_edge(title, UP, margin=0.5)

    # Lưu video:
    save_latest_video("Scene1_Final.mp4")
"""

from manim import *
import numpy as np
import os
import shutil
import glob


# =============================================================================
# SPACING CONSTANTS
# =============================================================================
MARGIN_SM = 0.3       # Margin nhỏ
MARGIN_MD = 0.5       # Margin trung bình
MARGIN_LG = 0.8       # Margin lớn
MARGIN_XL = 1.2       # Margin rất lớn

PADDING_SM = 0.2
PADDING_MD = 0.4
PADDING_LG = 0.6

# Kích thước frame Manim mặc định
FRAME_W = config.frame_width    # 14.22 (default)
FRAME_H = config.frame_height   # 8.0 (default)

# Vùng an toàn (tránh bị cắt ở mép)
SAFE_MARGIN = 0.6
SAFE_LEFT = LEFT * (FRAME_W / 2 - SAFE_MARGIN)
SAFE_RIGHT = RIGHT * (FRAME_W / 2 - SAFE_MARGIN)
SAFE_TOP = UP * (FRAME_H / 2 - SAFE_MARGIN)
SAFE_BOTTOM = DOWN * (FRAME_H / 2 - SAFE_MARGIN)


# =============================================================================
# LAYOUT FUNCTIONS
# =============================================================================

def arrange_in_grid(mobjects: list, rows: int = None, cols: int = None,
                    buff_x: float = 0.5, buff_y: float = 0.5,
                    center: bool = True) -> VGroup:
    """
    Xếp danh sách mobjects thành lưới.

    Args:
        mobjects: Danh sách Mobjects
        rows: Số hàng (None = tự tính)
        cols: Số cột (None = tự tính)
        buff_x: Khoảng cách ngang
        buff_y: Khoảng cách dọc
        center: Có căn giữa màn hình không

    Returns:
        VGroup chứa tất cả mobjects đã sắp xếp
    """
    n = len(mobjects)
    if rows is None and cols is None:
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
    elif rows is None:
        rows = int(np.ceil(n / cols))
    elif cols is None:
        cols = int(np.ceil(n / rows))

    group = VGroup(*mobjects)
    group.arrange_in_grid(rows=rows, cols=cols, buff=(buff_x, buff_y))

    if center:
        group.move_to(ORIGIN)

    return group


def arrange_row(mobjects: list, buff: float = 0.5,
                center: bool = True) -> VGroup:
    """Xếp mobjects thành hàng ngang."""
    group = VGroup(*mobjects).arrange(RIGHT, buff=buff)
    if center:
        group.move_to(ORIGIN)
    return group


def arrange_column(mobjects: list, buff: float = 0.5,
                   center: bool = True) -> VGroup:
    """Xếp mobjects thành cột dọc."""
    group = VGroup(*mobjects).arrange(DOWN, buff=buff)
    if center:
        group.move_to(ORIGIN)
    return group


def pin_to_edge(mobject: Mobject, edge, margin: float = SAFE_MARGIN) -> Mobject:
    """
    Đặt mobject sát cạnh màn hình (có margin an toàn).

    Args:
        mobject: Object cần đặt
        edge: UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR
        margin: Khoảng cách từ cạnh

    Returns:
        Mobject đã được di chuyển (in-place)
    """
    mobject.to_edge(edge, buff=margin)
    return mobject


def split_screen_left_right(left_mob: Mobject, right_mob: Mobject,
                             gap: float = 0.5) -> VGroup:
    """
    Chia màn hình thành 2 nửa trái-phải.

    Args:
        left_mob: Object bên trái
        right_mob: Object bên phải
        gap: Khoảng cách giữa 2 bên

    Returns:
        VGroup chứa cả 2
    """
    half_w = FRAME_W / 4
    left_mob.move_to(LEFT * half_w)
    right_mob.move_to(RIGHT * half_w)
    return VGroup(left_mob, right_mob)


def split_screen_top_bottom(top_mob: Mobject, bottom_mob: Mobject,
                             gap: float = 0.5) -> VGroup:
    """
    Chia màn hình thành 2 nửa trên-dưới.

    Args:
        top_mob: Object phía trên
        bottom_mob: Object phía dưới
        gap: Khoảng cách giữa 2 phần

    Returns:
        VGroup chứa cả 2
    """
    quarter_h = FRAME_H / 4
    top_mob.move_to(UP * quarter_h)
    bottom_mob.move_to(DOWN * quarter_h)
    return VGroup(top_mob, bottom_mob)


def get_screen_region(position: str = "center") -> np.ndarray:
    """
    Trả về tọa độ trung tâm của vùng trên màn hình.

    Args:
        position: "center", "top", "bottom", "left", "right",
                  "top_left", "top_right", "bottom_left", "bottom_right"

    Returns:
        numpy array tọa độ [x, y, 0]
    """
    regions = {
        "center": ORIGIN,
        "top": UP * FRAME_H / 4,
        "bottom": DOWN * FRAME_H / 4,
        "left": LEFT * FRAME_W / 4,
        "right": RIGHT * FRAME_W / 4,
        "top_left": UP * FRAME_H / 4 + LEFT * FRAME_W / 4,
        "top_right": UP * FRAME_H / 4 + RIGHT * FRAME_W / 4,
        "bottom_left": DOWN * FRAME_H / 4 + LEFT * FRAME_W / 4,
        "bottom_right": DOWN * FRAME_H / 4 + RIGHT * FRAME_W / 4,
    }
    return regions.get(position, ORIGIN)


# =============================================================================
# VIDEO EXPORT / SAVE HELPER
# =============================================================================

def save_latest_video(filename: str = "output_video.mp4", output_dir: str = "exports",
                      open_folder: bool = True) -> str:
    """
    Tự động tìm video vừa render mới nhất (trong media/jupyter hoặc media/videos)
    và lưu/copy vào thư mục output_dir với tên mong muốn.

    Args:
        filename: Tên file đích (VD: "Scene1_Final.mp4")
        output_dir: Thư mục lưu (mặc định: "exports")
        open_folder: Tự động mở thư mục trong File Explorer sau khi lưu

    Returns:
        Đường dẫn tuyệt đối file video đã lưu
    """
    if not filename.endswith(".mp4"):
        filename += ".mp4"

    os.makedirs(output_dir, exist_ok=True)

    # Tìm tất cả file mp4 hoàn chỉnh (loại bỏ partial_movie_files)
    mp4_files = [
        f for f in glob.glob("media/**/*.mp4", recursive=True)
        if "partial_movie_files" not in f and not os.path.basename(f).startswith(".")
    ]

    if not mp4_files:
        print("[WARNING] Khong tim thay file video nao trong thu muc media/. Hay chay render scene truoc!")
        return None

    # Lấy file có thời gian chỉnh sửa mới nhất
    latest_file = max(mp4_files, key=os.path.getmtime)
    dest_path = os.path.join(output_dir, filename)

    shutil.copy2(latest_file, dest_path)
    file_size_mb = os.path.getsize(dest_path) / (1024 * 1024)

    abs_dest = os.path.abspath(dest_path)
    print("=" * 60)
    print(">>> DA LUU VIDEO THANH CONG!")
    print(f"  * Ten file  : {filename}")
    print(f"  * Vi tri    : {abs_dest}")
    print(f"  * Dung luong: {file_size_mb:.2f} MB")
    print("=" * 60)

    if open_folder:
        try:
            os.startfile(os.path.abspath(output_dir))
        except Exception:
            pass

    return abs_dest
