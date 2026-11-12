# テンポ社トップのヒーロー動画（試作）を作る
#   コンセプト：「想いをカタチにする」＝ 設計図の線が描かれ → 実際の施工写真に変わる
#   使い方: ~/venv/bin/python _video/make_hero.py  → _video/hero_draft.mp4
import os, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from lines import W, H, BW, BH, load_cover, line_strength, blur

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_video', 'hero_draft.mp4')
FPS = 30

# 場面：写真・切り抜き位置（左右, 上下）
SCENES = [
    ('images/keepcolor/IMG_3897.jpg', 0.5, 0.25),   # 店舗
    ('images/koiki/koiki_1.jpg',      0.5, 0.45),   # 住宅
    ('images/murakou/murakou_1.jpg',  0.5, 0.40),   # 内装
]

# 1場面の時間割（秒）
T_DRAW, T_HOLD, T_MORPH, T_PHOTO, T_OUT = 2.2, 0.4, 1.3, 1.3, 0.7
SCENE_LEN = T_DRAW + T_HOLD + T_MORPH + T_PHOTO + T_OUT
# 最後のロゴ場面（秒）：紺→白の紙 / ロゴの線を描く / 色が付く / 見せる / 紺に戻る（ループのつなぎ）
L_TO_WHITE, L_DRAW, L_FILL, L_HOLD, L_BACK = 0.8, 1.3, 0.8, 2.0, 0.8
TAIL = L_TO_WHITE + L_DRAW + L_FILL + L_HOLD + L_BACK
WHITE = np.array([248, 247, 243], np.float32)   # ロゴ用の白い紙
LOGO_INK = np.array([16, 56, 120], np.float32)  # ロゴの線（ロゴの紺）
LOGO_W = 1100                                   # 画面幅1920に対するロゴの幅（スマホで左右が切れても収まる大きさ）

PAPER = np.array([31, 47, 69], np.float32)     # 設計図の紺
INK = np.array([236, 242, 248], np.float32)    # 白い線

def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)

def make_paper():
    """紺の紙に、うっすら方眼と紙の粒子を入れる"""
    rng = np.random.default_rng(1)
    p = np.ones((BH, BW, 3), np.float32) * PAPER
    grid = np.zeros((BH, BW), np.float32)
    step = 48
    grid[::step, :] = 1; grid[:, ::step] = 1
    grid[::step * 4, :] = 2.2; grid[:, ::step * 4] = 2.2
    p += grid[..., None] * 5
    noise = blur((rng.random((BH, BW)) * 255).astype(np.uint8), 1.2) / 255.0 - 0.5
    p += noise[..., None] * 10
    return np.clip(p, 0, 255)

def reveal_field(seed):
    """線が描かれていく順番（左から、少しゆらぎを持たせて）"""
    rng = np.random.default_rng(seed)
    n = blur((rng.random((BH, BW)) * 255).astype(np.uint8), 60) / 255.0
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    x = np.linspace(0, 1, BW, dtype=np.float32)[None, :]
    y = np.linspace(0, 1, BH, dtype=np.float32)[:, None]
    f = 0.62 * x + 0.13 * y + 0.25 * n
    return (f - f.min()) / (f.max() - f.min())

def zoom_crop(img, z):
    """z: 0→1 でゆっくり寄っていく"""
    s = 1 + (BW / W - 1) * z
    cw, ch = BW / s, BH / s
    x0, y0 = (BW - cw) / 2, (BH - ch) / 2
    return Image.fromarray(img).resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

def make_logo():
    """ロゴを画面中央に置いた絵（色付き）・不透明度・輪郭線を作る"""
    lg = Image.open(os.path.join(ROOT, 'logo.png')).convert('RGBA')
    lg = lg.crop(lg.getbbox())
    lg = lg.resize((LOGO_W, round(lg.height * LOGO_W / lg.width)), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2), lg)
    a = np.asarray(canvas, np.float32)
    rgb, alpha = a[..., :3], a[..., 3:] / 255.0
    # 白地に置いたロゴから輪郭を取り、線だけの状態を作る
    on_white = Image.fromarray((rgb * alpha + 255 * (1 - alpha)).astype(np.uint8))
    g = np.asarray(on_white.convert('L'))
    edge = np.abs(blur(g, 1.0) - blur(g, 2.6))
    edge = np.clip(edge / (np.percentile(edge, 99.5) + 1e-6) * 1.4, 0, 1)[..., None]
    rng = np.random.default_rng(3)
    n = blur((rng.random((H, W)) * 255).astype(np.uint8), 40) / 255.0
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    x = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    f = 0.8 * x + 0.2 * n
    field = (f - f.min()) / (f.max() - f.min())
    return rgb, alpha, edge, field

def logo_frame(u, paper_flat, white, logo):
    rgb, alpha, edge, field = logo
    to_white = ease(u / L_TO_WHITE)
    draw = ease((u - L_TO_WHITE) / L_DRAW)
    fill = ease((u - L_TO_WHITE - L_DRAW) / L_FILL)
    back = ease((u - TAIL + L_BACK) / L_BACK)
    img = paper_flat * (1 - to_white) + white * to_white
    vis = np.clip((draw * 1.12 - field) / 0.05, 0, 1)[..., None]
    line_a = edge * vis * (1 - fill)
    img = img * (1 - line_a) + LOGO_INK * line_a
    fa = alpha * fill
    img = img * (1 - fa) + rgb * fa
    img = img * (1 - back) + paper_flat * back
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def main():
    paper = make_paper()
    logo = make_logo()
    white = np.ones((H, W, 3), np.float32) * WHITE
    scenes = []
    for i, (path, fx, fy) in enumerate(SCENES):
        ph = load_cover(os.path.join(ROOT, path), fx, fy)
        scenes.append((np.asarray(ph, np.float32), line_strength(ph)[..., None], reveal_field(i + 7)))
        print('準備OK', path)

    total = SCENE_LEN * len(scenes) + TAIL
    nframes = round(total * FPS)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p',
           '-tune', 'film', '-movflags', '+faststart', '-an', OUT]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    paper_flat_img = zoom_crop(paper.astype(np.uint8), 0)
    paper_flat = np.asarray(paper_flat_img, np.float32)
    for k in range(nframes):
        t = k / FPS
        si = int(t // SCENE_LEN)
        if si >= len(scenes):
            frame = logo_frame(t - SCENE_LEN * len(scenes), paper_flat, white, logo)
        else:
            photo, lines, field = scenes[si]
            u = t - si * SCENE_LEN
            draw = ease(u / T_DRAW)
            morph = ease((u - T_DRAW - T_HOLD) / T_MORPH)
            out = ease((u - SCENE_LEN + T_OUT) / T_OUT)
            # 線を描いていく（境目は少しぼかす）
            vis = np.clip((draw * 1.12 - field) / 0.05, 0, 1)[..., None]
            line_a = lines * vis * (1 - ease((u - T_DRAW - T_HOLD - 0.4) / T_MORPH))
            base = paper * (1 - morph) + photo * morph
            img = base * (1 - line_a) + INK * line_a
            # 線を描き終えてから寄り始める（紙の方眼が場面の切り替えで跳ねないように）
            z = ease((u - T_DRAW) / (SCENE_LEN - T_DRAW))
            zf = np.asarray(zoom_crop(np.clip(img, 0, 255).astype(np.uint8), z), np.float32)
            frame = Image.fromarray((zf * (1 - out) + paper_flat * out).astype(np.uint8))
        enc.stdin.write(frame.tobytes())
        if k % 60 == 0:
            print(f'{k}/{nframes}', flush=True)
    enc.stdin.close(); enc.wait()
    print('できました', OUT, f'{os.path.getsize(OUT)/1e6:.1f}MB', f'{total:.1f}秒')

if __name__ == '__main__':
    main()
