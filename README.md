# Manim Video Production — Boilerplate Project

Project Manim Community Edition có cấu trúc module hóa, sẵn sàng để tạo bất kỳ video animation nào.

## Cài đặt

### 1. Cài Manim Community Edition

```bash
pip install manim
```

> **Lưu ý**: Manim cần một số phụ thuộc hệ thống (LaTeX, FFmpeg, Cairo).
> Xem hướng dẫn đầy đủ: https://docs.manim.community/en/stable/installation.html

### 2. Cài dependencies project

```bash
pip install -r requirements.txt
```

## Cấu trúc Project

```
├── main.py              # Entry point & hướng dẫn CLI
├── config.py            # Cấu hình toàn cục (màu, font, timing...)
│
├── components/          # Mobjects tái sử dụng
│   ├── text_styles.py   # Title, Subtitle, Caption, BulletList...
│   ├── boxes.py         # InfoBox, HighlightBox, CodeBlock, GlassPanel
│   └── arrows_labels.py # LabeledArrow, BraceAnnotation, Callout
│
├── utils/               # Tiện ích
│   ├── colors.py        # Bảng màu thống nhất
│   ├── animations.py    # Custom animations
│   └── layout.py        # Layout helpers
│
├── scenes/              # Scene files (thêm vào đây)
│   └── example_scene.py # Scene mẫu
│
└── assets/              # Hình ảnh, font, SVG
```

## Cách sử dụng

### Chạy scene mẫu

```bash
# Preview nhanh (chất lượng thấp)
manim -pql scenes/example_scene.py ExampleScene

# Chất lượng cao (1080p)
manim -pqh scenes/example_scene.py ExampleScene
```

### Tạo scene mới

1. Tạo file trong `scenes/`, ví dụ `scenes/my_scene.py`:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from config import *
from utils import *
from components import *

class MyScene(Scene):
    def construct(self):
        apply_scene_config(self)

        title = StyledTitle("Hello World")
        self.play(fade_in_shift(title))
        self.wait(2)
        self.play(FadeOut(title))
```

2. Render:

```bash
manim -pql scenes/my_scene.py MyScene
```

## Components có sẵn

| Component | Mô tả |
|-----------|--------|
| `StyledTitle` | Tiêu đề lớn, đậm |
| `StyledSubtitle` | Phụ đề |
| `StyledHeading` | Heading section |
| `StyledBody` | Text nội dung |
| `StyledCaption` | Chú thích nhỏ |
| `BulletList` | Danh sách bullet points |
| `SectionTitle` | Tiêu đề section có gạch dưới |
| `InfoBox` | Hộp thông tin có title + content |
| `HighlightBox` | Hộp highlight bao quanh object |
| `CodeBlock` | Code block kiểu editor |
| `GlassPanel` | Panel glassmorphism |
| `LabeledArrow` | Mũi tên có nhãn |
| `BraceAnnotation` | Ngoặc nhọn có text |
| `Callout` | Tooltip/speech bubble |
| `DashedConnection` | Đường nét đứt nối 2 objects |

## Custom Animations có sẵn

| Animation | Mô tả |
|-----------|--------|
| `fade_in_shift()` | Fade in kèm dịch chuyển |
| `fade_out_shift()` | Fade out kèm dịch chuyển |
| `sequential_fade_in()` | Fade in lần lượt nhiều objects |
| `highlight_pulse()` | Nhấp nháy phóng to/thu nhỏ |
| `sweep_in()` | Quét vào từ ngoài màn hình |
| `typewriter_text()` | Hiệu ứng đánh máy |
| `scale_fade_in()` | Pop-in (scale + fade) |
| `blink()` | Nhấp nháy ẩn/hiện |
| `draw_then_fade()` | Vẽ → giữ → fade out |

## Quality Flags

| Flag | Độ phân giải | FPS |
|------|-------------|-----|
| `-ql` | 480p | 15 |
| `-qm` | 720p | 30 |
| `-qh` | 1080p | 60 |
| `-qk` | 2160p (4K) | 60 |
