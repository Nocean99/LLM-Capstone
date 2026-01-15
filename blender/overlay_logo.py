from PIL import Image

# Load images
album = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\album cover.png").convert("RGBA")
logo_full = Image.open(r"C:\Users\noahs\Desktop\ai experiments\blender\nocean_name.png").convert("RGBA")

# Get dimensions
album_w, album_h = album.size
logo_w, logo_h = logo_full.size

# Crop to get just the TOP logo (white text on black - top half of image)
top_logo = logo_full.crop((0, 0, logo_w, logo_h // 2))

# Now extract just the logo part without excess black
# Find bounding box of non-black pixels
pixels = top_logo.load()
min_x, min_y, max_x, max_y = logo_w, logo_h // 2, 0, 0

for y in range(top_logo.height):
    for x in range(top_logo.width):
        r, g, b, a = pixels[x, y]
        # If not pure black
        if r > 10 or g > 10 or b > 10:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

# Add padding
padding = 10
min_x = max(0, min_x - padding)
min_y = max(0, min_y - padding)
max_x = min(top_logo.width, max_x + padding)
max_y = min(top_logo.height, max_y + padding)

# Crop to just the logo
logo_cropped = top_logo.crop((min_x, min_y, max_x, max_y))

# Make black pixels transparent
logo_data = logo_cropped.getdata()
new_data = []
for pixel in logo_data:
    r, g, b, a = pixel
    # If pixel is very dark (black background), make transparent
    if r < 15 and g < 15 and b < 15:
        new_data.append((0, 0, 0, 0))
    else:
        new_data.append(pixel)

logo_transparent = Image.new("RGBA", logo_cropped.size)
logo_transparent.putdata(new_data)

# Resize logo to fit nicely (about 40% of album width)
target_width = int(album_w * 0.5)
aspect = logo_transparent.height / logo_transparent.width
target_height = int(target_width * aspect)
logo_resized = logo_transparent.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Position at bottom center
x = (album_w - target_width) // 2
y = album_h - target_height - int(album_h * 0.08)  # 8% from bottom

# Composite
result = album.copy()
result.paste(logo_resized, (x, y), logo_resized)

# Save
output_path = r"C:\Users\noahs\Desktop\ai experiments\blender\album_cover_final.png"
result.save(output_path, "PNG")

print(f"Done! Saved to: {output_path}")
print(f"Album size: {album_w}x{album_h}")
print(f"Logo size: {target_width}x{target_height}")
print(f"Position: ({x}, {y})")
