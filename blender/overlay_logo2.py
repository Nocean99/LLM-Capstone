from PIL import Image

# Load images
album = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\album cover.png").convert("RGBA")
logo = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\nocean logo.png").convert("RGBA")

# Get dimensions
album_w, album_h = album.size
logo_w, logo_h = logo.size

# Make black/dark pixels transparent
logo_data = logo.getdata()
new_data = []
for pixel in logo_data:
    r, g, b, a = pixel
    # If pixel is very dark (black background), make transparent
    if r < 20 and g < 20 and b < 20:
        new_data.append((0, 0, 0, 0))
    else:
        new_data.append(pixel)

logo_transparent = Image.new("RGBA", logo.size)
logo_transparent.putdata(new_data)

# Resize logo to fit nicely (about 60% of album width)
target_width = int(album_w * 0.6)
aspect = logo_transparent.height / logo_transparent.width
target_height = int(target_width * aspect)
logo_resized = logo_transparent.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Position centered, slightly below middle (10% down from center)
x = (album_w - target_width) // 2
y = (album_h - target_height) // 2 + int(album_h * 0.10)

# Composite
result = album.copy()
result.paste(logo_resized, (x, y), logo_resized)

# Save
output_path = r"C:\Users\noahs\Desktop\ai experiments\blender\album_cover_final2.png"
result.save(output_path, "PNG")

print(f"Done! Saved to: {output_path}")
