import os
import requests

def download_font(font_url="https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf", font_name="Montserrat-Bold.ttf"):
    fonts_dir = "fonts"
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
        
    font_path = os.path.join(fonts_dir, font_name)
    if not os.path.exists(font_path):
        print(f"Downloading font {font_name}...")
        try:
            response = requests.get(font_url)
            response.raise_for_status()
            with open(font_path, "wb") as f:
                f.write(response.content)
            print("Font downloaded successfully.")
        except Exception as e:
            print(f"Failed to download font: {e}")
            return None
    return font_path
