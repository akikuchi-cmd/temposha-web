# 施工写真から「設計図の白い線画」を作る（試作用）
import numpy as np
from PIL import Image, ImageOps, ImageFilter

W, H = 1920, 1080
ZOOM = 1.08          # 拡大していく分の余白
BW, BH = round(W * ZOOM), round(H * ZOOM)

def load_cover(path, fx=0.5, fy=0.5):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    s = max(BW / im.width, BH / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - BW) * fx); y = round((im.height - BH) * fy)
    return im.crop((x, y, x + BW, y + BH))

def blur(a, r):
    return np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(r)), dtype=np.float32)

def line_strength(photo):
    g = np.asarray(photo.convert('L'), dtype=np.float32)
    g8 = g.astype(np.uint8)
    g1, g2 = blur(g8, 1.4), blur(g8, 3.2)
    d = np.abs(g1 - g2)                       # 輪郭の強さ（明暗差）
    d = d / (np.percentile(d, 99.3) + 1e-6)
    s = np.clip((d - 0.28) / 0.45, 0, 1)      # 弱い模様は消して輪郭だけ残す
    s = blur((s * 255).astype(np.uint8), 0.7) / 255.0
    return np.clip(s * 1.15, 0, 1)
