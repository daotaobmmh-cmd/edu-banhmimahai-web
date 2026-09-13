import os, shutil
from PIL import Image, ImageDraw, ImageFont

def make_kynangsale_banner():
    width = 1200
    height = 630

    # 1. Base vibrant orange background image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bg = Image.new("RGBA", (width, height))
    draw_bg = ImageDraw.Draw(bg)

    # Orange gradient: top-left #F26800 to bottom-right #D84800
    for y in range(height):
        r = int(242 - (242 - 216) * (y / height))
        g = int(104 - (104 - 72) * (y / height))
        b = int(0)
        draw_bg.line([(0, y), (width, y)], fill=(r, g, b, 255))

    img.paste(bg, (0, 0))

    # Decorative right side subtle curve accent
    curve_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_curve = ImageDraw.Draw(curve_overlay)
    draw_curve.ellipse([680, -140, 1540, 770], fill=(225, 78, 0, 80))
    img = Image.alpha_composite(img, curve_overlay)
    draw = ImageDraw.Draw(img)

    # 2. White logo card container
    card_x = 100
    card_y = 75
    card_w = 440
    card_h = 165
    card_radius = 32

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=card_radius,
        fill=(255, 255, 255, 255)
    )

    logo_path = os.path.join("nhuongquyen", "logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join("kynangsale", "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        target_h = 108
        aspect = logo.width / logo.height
        target_w = int(target_h * aspect)
        
        if target_w > (card_w - 40):
            target_w = card_w - 40
            target_h = int(target_w / aspect)

        logo_resized = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        l_x = card_x + (card_w - target_w) // 2
        l_y = card_y + (card_h - target_h) // 2
        img.paste(logo_resized, (l_x, l_y), logo_resized)
        draw = ImageDraw.Draw(img)

    # 3. Load font
    font_path = os.path.join("scratch", "fonts", "be_vietnam_black.ttf")
    if not os.path.exists(font_path):
        candidates = [
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\tahomabd.ttf",
            "C:\\Windows\\Fonts\\segoeuib.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                font_path = c
                break

    # Font size calculation: 18 characters in 1200px width
    # 70-74px fits perfectly with ~100px margins
    font_size = 72
    font_main = ImageFont.truetype(font_path, font_size)

    text_line1 = "TRANG BỊ KIẾN THỨC"
    text_line2 = "MỞ XE CHUẨN MÁ HẢI"

    text_x = 100
    line1_y = 295
    line2_y = 410

    # Drop shadows
    draw.text((text_x + 3, line1_y + 3), text_line1, fill=(140, 45, 0, 160), font=font_main)
    draw.text((text_x, line1_y), text_line1, fill=(255, 255, 255, 255), font=font_main)

    draw.text((text_x + 3, line2_y + 3), text_line2, fill=(140, 45, 0, 160), font=font_main)
    draw.text((text_x, line2_y), text_line2, fill=(254, 214, 55, 255), font=font_main)

    # Convert to RGB and save everywhere needed
    rgb_img = Image.new("RGB", (width, height), (234, 98, 0))
    rgb_img.paste(img, (0, 0), img)

    destinations = [
        os.path.join("kynangsale", "images", "og-banner-2026.png"),
        os.path.join("kynangsale", "images", "og-banner.png"),
        os.path.join("kynangsale", "images", "banner.png"),
        os.path.join("kynangsale", "og-banner-2026.png"),
        os.path.join("kynangsale", "og-banner.png"),
        os.path.join("kynangsale", "banner.png")
    ]

    for d in destinations:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        rgb_img.save(d, format="PNG", quality=100)
        print("Saved banner to:", d)

    # Also copy to artifact directory for inspection
    artifact_dir = r"C:\Users\admin\.gemini\antigravity\brain\da3eb171-3234-4d6a-bec4-5ead1d549214"
    artifact_banner = os.path.join(artifact_dir, "og_banner_kynangsale_verified.png")
    rgb_img.save(artifact_banner, format="PNG", quality=100)
    print("Saved artifact banner to:", artifact_banner)

if __name__ == "__main__":
    make_kynangsale_banner()
