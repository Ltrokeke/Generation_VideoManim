"""
colors.py — Bảng màu (Color Palette) thống nhất cho toàn bộ project.

Sử dụng:
    from utils.colors import *

    # Dùng trực tiếp
    circle = Circle(color=PRIMARY)
    text = Text("Hello", color=TEXT_PRIMARY)

    # Dùng helper
    faded = fade_color(PRIMARY, 0.5)
"""

from manim import *

# =============================================================================
# BACKGROUND
# =============================================================================
BG_DARK = "#0f0f1a"         # Nền tối chính
BG_MEDIUM = "#1a1a2e"       # Nền tối phụ (panel, box)
BG_LIGHT = "#2a2a3e"        # Nền nhạt hơn (hover, highlight area)

# =============================================================================
# PRIMARY PALETTE — Màu chủ đạo
# =============================================================================
PRIMARY = "#6c63ff"          # Tím xanh — màu chính
PRIMARY_LIGHT = "#8b83ff"    # Tím xanh nhạt
PRIMARY_DARK = "#4a42d4"     # Tím xanh đậm

# =============================================================================
# SECONDARY PALETTE
# =============================================================================
SECONDARY = "#00d2ff"        # Cyan — màu phụ
SECONDARY_LIGHT = "#5ce1ff"
SECONDARY_DARK = "#009ec2"

# =============================================================================
# ACCENT PALETTE
# =============================================================================
ACCENT = "#ff6b9d"           # Hồng coral — điểm nhấn
ACCENT_LIGHT = "#ff9dbf"
ACCENT_DARK = "#d4456e"

# =============================================================================
# SEMANTIC COLORS — Màu ngữ nghĩa
# =============================================================================
SUCCESS = "#00e676"          # Xanh lá — thành công
WARNING = "#ffab40"          # Cam — cảnh báo
ERROR = "#ff5252"            # Đỏ — lỗi
INFO = "#448aff"             # Xanh dương — thông tin

# =============================================================================
# TEXT COLORS
# =============================================================================
TEXT_PRIMARY = "#ffffff"     # Trắng — text chính
TEXT_SECONDARY = "#b0b0c8"   # Xám nhạt — text phụ
TEXT_MUTED = "#6a6a8a"       # Xám — text mờ, chú thích

# =============================================================================
# NODE / GRAPH COLORS — Dùng cho đồ thị, diagram
# =============================================================================
NODE_COLORS = [
    "#6c63ff",  # Tím
    "#00d2ff",  # Cyan
    "#ff6b9d",  # Hồng
    "#00e676",  # Xanh lá
    "#ffab40",  # Cam
    "#ff5252",  # Đỏ
    "#e040fb",  # Magenta
    "#40c4ff",  # Xanh nhạt
]

EDGE_COLOR = "#4a4a6a"       # Màu cạnh mặc định
EDGE_HIGHLIGHT = "#6c63ff"   # Màu cạnh khi highlight

# =============================================================================
# GRADIENT PRESETS
# =============================================================================
GRADIENT_PRIMARY = [PRIMARY, SECONDARY]
GRADIENT_WARM = [ACCENT, WARNING]
GRADIENT_COOL = [PRIMARY, "#00e5ff"]
GRADIENT_SUNSET = ["#ff6b6b", "#ffa06b", "#ffd96b"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def fade_color(color: str, opacity: float) -> str:
    """
    Trả về ManimColor với opacity đã chỉnh.

    Args:
        color: Hex color string (vd: "#6c63ff")
        opacity: 0.0 (trong suốt) đến 1.0 (đậm)

    Returns:
        ManimColor object với opacity tương ứng
    """
    return ManimColor(color).interpolate(ManimColor(BG_DARK), 1 - opacity)


def get_node_color(index: int) -> str:
    """Lấy màu cho node theo index, tự động lặp lại nếu vượt quá palette."""
    return NODE_COLORS[index % len(NODE_COLORS)]


def gradient_colors(color_start: str, color_end: str, steps: int) -> list:
    """
    Tạo danh sách màu gradient giữa 2 màu.

    Args:
        color_start: Hex color bắt đầu
        color_end: Hex color kết thúc
        steps: Số bước (số màu trả về)

    Returns:
        List các ManimColor
    """
    start = ManimColor(color_start)
    end = ManimColor(color_end)
    return [
        start.interpolate(end, i / max(steps - 1, 1))
        for i in range(steps)
    ]
