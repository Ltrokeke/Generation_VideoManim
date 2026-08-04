"""
config.py — Cấu hình toàn cục cho project Manim.

Tất cả scene nên import file này để đảm bảo tính nhất quán:
    from config import *

File này chứa:
    - Quality presets
    - Timing defaults (animation, wait, transition)
    - Font settings
    - Layout settings
"""

from manim import *
from utils.colors import *

# =============================================================================
# QUALITY PRESETS
# =============================================================================
# Sử dụng qua CLI flag:
#   -ql  → low quality (480p, 15fps)   — preview nhanh
#   -qm  → medium quality (720p, 30fps) — xem thử
#   -qh  → high quality (1080p, 60fps) — render final
#   -qp  → production (1440p, 60fps)
#   -qk  → 4K (2160p, 60fps)

# =============================================================================
# TIMING DEFAULTS (giây)
# =============================================================================
FADE_TIME = 0.7           # Thời gian fade in/out mặc định
WAIT_SHORT = 0.5          # Dừng ngắn
WAIT_MEDIUM = 1.0         # Dừng trung bình
WAIT_LONG = 2.0           # Dừng dài (đọc text)
WAIT_EXTRA_LONG = 3.0     # Dừng rất dài (đọc đoạn dài)
TRANSITION_TIME = 1.0     # Thời gian chuyển cảnh
ANIM_SPEED_FAST = 0.4     # Animation nhanh
ANIM_SPEED_NORMAL = 0.8   # Animation bình thường
ANIM_SPEED_SLOW = 1.5     # Animation chậm (giải thích chi tiết)

# =============================================================================
# FONT SETTINGS
# =============================================================================
FONT_DEFAULT = "sans-serif"  # Font chuẩn không bị lỗi kerning/spacing trong Pango trên Windows

# Font sizes (tỷ lệ cho Text mobject)
FONT_SIZE_TITLE = 56         # Tiêu đề chính
FONT_SIZE_SUBTITLE = 40      # Phụ đề
FONT_SIZE_HEADING = 36       # Heading
FONT_SIZE_BODY = 30          # Nội dung chính
FONT_SIZE_CAPTION = 24       # Chú thích
FONT_SIZE_SMALL = 20         # Text nhỏ
FONT_SIZE_TINY = 16          # Text rất nhỏ (annotation)

# Font weight
FONT_WEIGHT_NORMAL = NORMAL
FONT_WEIGHT_BOLD = BOLD

# =============================================================================
# BACKGROUND SETTINGS
# =============================================================================
BACKGROUND_COLOR = "#0f172a"   # Nền tối hiện đại (Slate-900)

# =============================================================================
# STROKE / LINE SETTINGS
# =============================================================================
STROKE_WIDTH_THIN = 1.5
STROKE_WIDTH_DEFAULT = 2.5
STROKE_WIDTH_THICK = 4.0
STROKE_WIDTH_BOLD = 6.0

# =============================================================================
# OBJECT DEFAULTS
# =============================================================================
DEFAULT_CIRCLE_RADIUS = 0.3
DEFAULT_DOT_RADIUS = 0.08
DEFAULT_RECT_CORNER_RADIUS = 0.15
DEFAULT_OPACITY = 0.9

# =============================================================================
# HELPER: Apply global config to a scene
# =============================================================================

def apply_scene_config(scene: Scene):
    """
    Áp dụng cấu hình toàn cục cho scene (Font Times New Roman, Background, Text color).
    Gọi ở đầu construct():

        def construct(self):
            apply_scene_config(self)
            ...
    """
    scene.camera.background_color = BACKGROUND_COLOR
    Text.set_default(font=FONT_DEFAULT, color=TEXT_PRIMARY)
