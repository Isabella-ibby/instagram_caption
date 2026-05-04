import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils import download_font

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        # Check width using getbbox or getlength
        # For multiline, we can just join and check width
        test_line = ' '.join(current_line)
        # PIL >= 8.0:
        if font.getlength(test_line) > max_width:
            if len(current_line) == 1:
                # Word itself is too long, force it
                lines.append(current_line[0])
                current_line = []
            else:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
        
    return lines

def create_gradient(width, height, color1, color2):
    """Generates a vertical gradient image."""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        # 255 at top (color2), 0 at bottom (color1)
        mask_data.extend([int(255 * (height - y) / height)] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def generate_poster(quote_text, mood, watermark_text, output_path="output.jpg"):
    # Size
    W, H = 1080, 1080
    
    # Mood palettes
    palettes = {
        "sad": [("#1e130c", "#9a8478"), ("#141e30", "#243b55"), ("#000000", "#434343")],
        "romantic": [("#ff7eb3", "#ff758c"), ("#ff0844", "#ffb199"), ("#a18cd1", "#fbc2eb")],
        "real": [("#232526", "#414345"), ("#2c3e50", "#3498db"), ("#111111", "#282828")],
        "deep": [("#1a1a2e", "#16213e"), ("#0f2027", "#203a43"), ("#2b5876", "#4e4376")]
    }
    
    # Default to "real" palette if mood is unknown
    selected_palette = random.choice(palettes.get(mood.lower(), palettes["real"]))
    
    c1, c2 = hex_to_rgb(selected_palette[0]), hex_to_rgb(selected_palette[1])
    
    # 1. Background
    img = create_gradient(W, H, c1, c2)
    
    # 2. Dark Overlay for readability
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 80)) # 80 alpha out of 255
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    
    # 3. Typography
    font_path = download_font()
    if not font_path:
        font_path = "arial.ttf" # Fallback
    
    # Try different sizes based on text length
    base_size = 70
    if len(quote_text) > 100:
        base_size = 60
    if len(quote_text) > 150:
        base_size = 50
        
    try:
        font = ImageFont.truetype(font_path, base_size)
    except:
        font = ImageFont.load_default()
        
    try:
        font_watermark = ImageFont.truetype(font_path, 30)
    except:
        font_watermark = ImageFont.load_default()
    
    # 4. Text Wrapping
    max_text_width = W - 200 # 100px padding on each side
    lines = wrap_text(quote_text, font, max_text_width)
    
    # Calculate total text height
    line_spacing = 20
    # PIL getbbox returns (left, top, right, bottom)
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
    
    # 5. Draw Text (Centered)
    current_y = (H - total_text_height) // 2
    
    for line in lines:
        line_width = font.getlength(line)
        x = (W - line_width) // 2
        
        # Simple drop shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, current_y + shadow_offset), line, font=font, fill=(0, 0, 0, 150))
        # Actual text
        draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += font.getbbox(line)[3] - font.getbbox(line)[1] + line_spacing
        
    # 6. Watermark (Bottom Center)
    if watermark_text:
        w_width = font_watermark.getlength(watermark_text)
        w_x = (W - w_width) // 2
        w_y = H - 100
        draw.text((w_x, w_y), watermark_text, font=font_watermark, fill=(255, 255, 255, 180))
        
    # Save image
    img = img.convert('RGB')
    img.save(output_path, quality=95)
    return output_path

if __name__ == "__main__":
    generate_poster("Zindagi ek safar hai suhana, yahan kal kya ho kisne jaana.", "real", "@realtalks", "test_poster.jpg")
